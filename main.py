import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    if len(sys.argv) == 1:
        print ("Error: No prompt provided")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    prompt = sys.argv[1]
    #test_content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    ai_response = client.models.generate_content(model='gemini-2.0-flash-001', contents=prompt)
    
    print (f"Text returned is {ai_response.text}")
    #print (f"Metadata returned is {test.usage_metadata}")
    print (f"Prompt tokens: {ai_response.usage_metadata.prompt_token_count}")
    print (f"Response tokens: {ai_response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
