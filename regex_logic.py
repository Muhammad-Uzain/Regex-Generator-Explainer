import os
import re
import json

from google import genai
from dotenv import load_dotenv

# Load the variables written in the .env file into the environment.
load_dotenv()

# Read the key from the environment. NEVER hard-code the key here.
API_KEY = os.getenv("GEMINI_API_KEY")

# The model to use. Gemini Flash models are on the free tier. If this
# name ever stops working, open Google AI Studio (aistudio.google.com),
# check the current list of free models, and change this ONE line.
MODEL_NAME = "gemini-2.5-flash"

# Create the client once. If the key is missing we keep it as None and
# report that clearly inside generate_regex (instead of crashing).
client = genai.Client(api_key=API_KEY) if API_KEY else None


def generate_regex(description):
    """Turn a plain-English description into a regex + explanation."""

    # Guard 1: was the API key actually loaded?
    if client is None:
        return {
            "success": False,
            "pattern": None,
            "explanation": None,
            "error": "API key not found. Add GEMINI_API_KEY to your .env file.",
        }

    # Build the prompt. We insist on JSON ONLY, in a fixed shape, so the
    # program can read the fields reliably.
    prompt = (
        "You are a regular-expression expert.\n"
        "The user will describe, in plain English, a text pattern they "
        "want to match.\n"
        "Return ONE regular expression in Python re syntax that matches "
        "it, plus a breakdown of each part.\n\n"
        'User description: "' + description + '"\n\n'
        "Respond with ONLY a JSON object. No markdown, no backticks, no "
        "text before or after. Use exactly this shape:\n"
        "{\n"
        '  "pattern": "the regex as a string",\n'
        '  "explanation": [\n'
        '    {"part": "a piece of the pattern", "meaning": "what it does"}\n'
        "  ]\n"
        "}\n"
    )

    # Call the API and parse the reply, catching every kind of failure.
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        raw = response.text.strip()

        # Models sometimes wrap JSON in ```json ... ``` fences. Strip them.
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lstrip().lower().startswith("json"):
                raw = raw.lstrip()[4:]
            raw = raw.strip()

        data = json.loads(raw)

        pattern = data.get("pattern")
        explanation = data.get("explanation", [])

        if not pattern:
            return {
                "success": False,
                "pattern": None,
                "explanation": None,
                "error": "The AI did not return a pattern. Try rephrasing.",
            }

        return {
            "success": True,
            "pattern": pattern,
            "explanation": explanation,
            "error": None,
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "pattern": None,
            "explanation": None,
            "error": "The AI's reply was not valid JSON. Please try again.",
        }
    except Exception as error:
        return {
            "success": False,
            "pattern": None,
            "explanation": None,
            "error": "Could not reach the AI service: " + str(error),
        }


def test_regex(pattern, test_strings):
    """Run pattern against each test string; report match / no match."""

    # Compile once. If the pattern is broken, report it cleanly per row.
    try:
        compiled = re.compile(pattern)
    except re.error as error:
        return [
            {"text": s, "matches": False, "error": "Invalid pattern: " + str(error)}
            for s in test_strings
        ]

    results = []
    for s in test_strings:
        # .search() looks for the pattern ANYWHERE inside the string.
        matched = compiled.search(s) is not None
        results.append({"text": s, "matches": matched})
    return results