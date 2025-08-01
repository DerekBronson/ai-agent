import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified python file and includes any additional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="List of optional arguments to use when running the specified python file",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    working_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_abs, file_path))

    if not target_file.startswith(working_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    full_args = ["python", target_file]
    for a in args:
        full_args.append(a)

    try:
        result = subprocess.run(
            full_args, cwd=working_directory, capture_output=True, timeout=30
        )
        if result == "":
            return "No output produced"
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        else:
            return f"STDOUT: {result.stdout}\\n STDERR: {result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

