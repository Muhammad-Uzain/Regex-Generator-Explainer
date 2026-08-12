"""
test_call.py  -  a quick check that your key and the SDK work.
Run:  python test_call.py
Delete this file once it works; it is not part of the final app.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("No API key found. Add GEMINI_API_KEY to your .env file.")
    raise SystemExit

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Say hello in one short sentence.",
)
print(response.text)