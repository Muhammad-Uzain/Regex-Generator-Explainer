"""
app.py  -  the Streamlit user interface.
Run it from the project folder with:   streamlit run app.py
"""

import streamlit as st

# The engine. While building the UI, comment the first line and use the
# second so you do not need an API key.

#import regex_logic as logic
import mock_logic as logic


# ---- Page setup ------------------------------------------------------
st.set_page_config(
    page_title="Regex Generator & Explainer",
    page_icon=":mag:",
    layout="centered",
)

st.title("Regex Generator & Explainer")
st.write(
    "Describe the text pattern you want to match in plain English. "
    "The app generates a regular expression, explains each part, and "
    "tests it against your sample strings."
)


# ---- Session state ---------------------------------------------------
# Streamlit re-runs this whole file on every click, so we store the
# result in st.session_state to keep it on screen between interactions.
if "result" not in st.session_state:
    st.session_state.result = None


# ---- Input widgets ---------------------------------------------------
description = st.text_input(
    "What do you want to match?",
    placeholder="e.g. an email address",
)

test_input = st.text_area(
    "Test strings (one per line) - optional",
    placeholder="john@example.com\nnot-an-email\nhello@world.co",
    height=120,
)

generate_clicked = st.button("Generate regex", type="primary")


# ---- Handle the click ------------------------------------------------
if generate_clicked:
    # Input validation: do not call the engine on empty input.
    if not description.strip():
        st.warning("Please enter a description first.")
    else:
        with st.spinner("Asking the AI..."):
            st.session_state.result = logic.generate_regex(description)


# ---- Show the result -------------------------------------------------
result = st.session_state.result

if result is not None:
    if not result["success"]:
        # Something went wrong - show the friendly message from the engine.
        st.error(result["error"])
    else:
        st.divider()

        # 1) The pattern, in a copy-friendly code box.
        st.subheader("Pattern")
        st.code(result["pattern"], language="text")

        # 2) The explanation, part by part.
        st.subheader("Explanation")
        for item in result["explanation"]:
            st.markdown("- `" + item["part"] + "` - " + item["meaning"])

        # 3) Test the pattern against the user's sample strings.
        test_strings = [ln for ln in test_input.splitlines() if ln.strip()]
        if test_strings:
            st.subheader("Test results")
            checks = logic.test_regex(result["pattern"], test_strings)
            for check in checks:
                if check.get("error"):
                    st.error(check["error"])
                elif check["matches"]:
                    st.success("Match:  " + check["text"])
                else:
                    st.write("No match:  " + check["text"])
