"""
mock_logic.py  -  a FAKE engine for building the UI.
Same two functions as regex_logic.py, same return shapes, but it returns
hard-coded data instantly. No API key needed.

To switch between fake and real, change ONE line at the top of app.py:
    import regex_logic as logic      # real engine
    # import mock_logic as logic     # fake engine
"""

import re
import time


def generate_regex(description):
    time.sleep(1)  # pretend the network took a moment, to show the spinner

    if not description.strip():
        return {
            "success": False,
            "pattern": None,
            "explanation": None,
            "error": "Please describe the pattern you want.",
        }

    return {
        "success": True,
        "pattern": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "explanation": [
            {"part": "[A-Za-z0-9._%+-]+", "meaning": "the name before the @"},
            {"part": "@", "meaning": "a literal @ symbol"},
            {"part": "[A-Za-z0-9.-]+", "meaning": "the domain name"},
            {"part": r"\.", "meaning": "a literal dot"},
            {"part": "[A-Za-z]{2,}", "meaning": "the extension, e.g. com"},
        ],
        "error": None,
    }


def test_regex(pattern, test_strings):
    try:
        compiled = re.compile(pattern)
    except re.error as error:
        return [
            {"text": s, "matches": False, "error": "Invalid pattern: " + str(error)}
            for s in test_strings
        ]
    return [
        {"text": s, "matches": compiled.search(s) is not None}
        for s in test_strings
    ]
