import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" --verbose')
        print('Example: python main.py "How do I build a calculator app"')
        sys.exit(1)

    prompt = " ".join(args)
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        Start by getting a list of all files and directories so you have the proper context to answer questions.
        """

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    for i in range(20):
        try:
            ai_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            for response in ai_response.candidates:
                messages.append(response.content)

            if ai_response.function_calls:
                for func in ai_response.function_calls:
                    func_results = call_function(func, verbose)
                    if not func_results.parts[0].function_response.response:
                        raise Exception(f"Error with response from {func.name}")
                    if verbose:
                        print(f"-> {func_results.parts[0].function_response.response}")
                    messages.append(func_results)
            else:
                print ("Final Response:\n")
                print (ai_response.text)
                break
        except Exception as e:
            return (f"There was an error processing the request: {e}")

    if verbose:
        print(f"User prompt: {prompt}\n")
        print(f"Prompt tokens: {ai_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {ai_response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    if function_call_part.name not in available_functions.keys():
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_to_call = available_functions[function_call_part.name]
    func_args = function_call_part.args
    func_args["working_directory"] = "./calculator"

    func_results = func_to_call(**func_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": func_results},
            )
        ],
    )


if __name__ == "__main__":
    main()
