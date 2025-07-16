import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    client = genai.Client(api_key=api_key)
    test_content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    test = client.models.generate_content(model='gemini-2.0-flash-001', contents=test_content)
    
    print (f"Text returned is {test.text}")
    metadata = test.usage_metadata
    print (f"Prompt tokens: {metadata["prompt_token_count"]}")
    print (f"Response tokens: {metadata["candidates_token_count"]}")

if __name__ == "__main__":
    main()
