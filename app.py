"""
app.py  -  the Streamlit user interface.
Run it from the project folder with:   streamlit run app.py
"""

import html
import streamlit as st

# The engine. Comment the first line and use the second to build the UI
# without an API key (the mock returns fake data instantly).
import regex_logic as logic
# import mock_logic as logic


# ---- Page config -----------------------------------------------------
st.set_page_config(
    page_title="Regex Generator & Explainer",
    page_icon=":mag:",
    layout="wide",          # gives room for the two side-by-side columns
)

# ---- A little CSS just to tidy spacing (cosmetic, safe to ignore) -----
st.markdown(
    """
    <style>
      .block-container {padding-top: 4rem; padding-bottom: 2rem; max-width: 1150px;}
      div[data-testid="stTextInput"] label,
      div[data-testid="stTextArea"] label {font-weight: 600;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Header (full width) ---------------------------------------------
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:14px; margin-bottom:4px;">
      <div style="font-family:'Courier New',monospace; font-size:26px; font-weight:800;
                  color:#0d1117; background:#2dd4bf; border-radius:10px;
                  padding:2px 12px; line-height:1.25;">&lt;/&gt;</div>
      <div>
        <div style="font-size:30px; font-weight:800; line-height:1.1;">
          Regex Generator <span style="color:#2dd4bf;">&amp;</span> Explainer
        </div>
        <div style="color:#8b949e; font-size:14px; margin-top:2px;">
          Describe a pattern in plain English &mdash; get a regex, an explanation,
          and a live match test.
        </div>
      </div>
    </div>
    <hr style="border:none; border-top:1px solid rgba(45,212,191,0.35); margin:10px 0 18px;">
    """,
    unsafe_allow_html=True,
)

# ---- Session state ---------------------------------------------------
# Streamlit re-runs the whole file on every click, so we keep the last
# result in session_state to hold it on screen between interactions.
if "result" not in st.session_state:
    st.session_state.result = None


# ---- Helper: build one colour-coded result row -----------------------
def result_card(text, matched):
    """Return HTML for a single test-result row (green if matched, red if not)."""
    text = html.escape(text)
    if matched:
        bg, line, accent, icon, label = (
            "rgba(46,160,67,0.15)", "#3fb950", "#3fb950", "&#10003;", "MATCH")
    else:
        bg, line, accent, icon, label = (
            "rgba(248,81,73,0.13)", "#f85149", "#f85149", "&#10007;", "NO MATCH")
    return (
        f'<div style="display:flex; align-items:center; gap:10px; background:{bg};'
        f' border:1px solid {line}55; border-left:4px solid {line};'
        f' border-radius:8px; padding:10px 14px; margin-bottom:8px;">'
        f'<span style="color:{accent}; font-weight:800; font-size:15px;">{icon}</span>'
        f'<span style="font-family:\'Courier New\',monospace; font-size:13px;'
        f' word-break:break-all;">{text}</span>'
        f'<span style="margin-left:auto; color:{accent}; font-size:11px;'
        f' font-weight:700; letter-spacing:.08em;">{label}</span>'
        f'</div>'
    )


# ---- Two columns: inputs (left)  |  results (right) -------------------
col_input, col_output = st.columns([1, 1.15], gap="large")

# ===== LEFT: the input form =====
with col_input:
    st.markdown("##### 1. Describe what to match")
    description = st.text_input(
        "What do you want to match?",
        placeholder="e.g. an email address",
    )
    test_input = st.text_area(
        "Test strings (one per line) - optional",
        placeholder="john@example.com\nnot-an-email\nhello@world.co",
        height=170,
    )
    generate_clicked = st.button(
        "Generate regex", type="primary", use_container_width=True
    )

    if generate_clicked:
        # Input validation: do not call the engine on empty input.
        if not description.strip():
            st.warning("Please enter a description first.")
        else:
            with st.spinner("Asking the AI..."):
                st.session_state.result = logic.generate_regex(description)

# ===== RIGHT: the results panel =====
with col_output:
    result = st.session_state.result

    if result is None:
        # Empty state so the panel is not blank before the first run.
        st.markdown(
            '<div style="border:1px dashed rgba(139,148,158,0.4); border-radius:12px;'
            ' padding:48px 20px; text-align:center; color:#8b949e; margin-top:6px;">'
            '<div style="font-family:\'Courier New\',monospace; font-size:30px;'
            ' color:#2dd4bf; margin-bottom:8px;">{ }</div>'
            'Your pattern, explanation, and test results will appear here.'
            '</div>',
            unsafe_allow_html=True,
        )

    elif not result["success"]:
        # Friendly error card (never a raw crash).
        st.markdown(
            f'<div style="background:rgba(248,81,73,0.13); border:1px solid #f8514955;'
            f' border-left:4px solid #f85149; border-radius:8px; padding:14px 16px;'
            f' color:#f85149;"><b>Error:</b> {html.escape(result["error"])}</div>',
            unsafe_allow_html=True,
        )

    else:
        # 1) The pattern, in a copy-friendly code box.
        st.markdown("##### Pattern")
        st.code(result["pattern"], language="text")

        # 2) The explanation, one part at a time, as monospace chips.
        st.markdown("##### Explanation")
        rows = ""
        for item in result["explanation"]:
            part = html.escape(str(item.get("part", "")))
            meaning = html.escape(str(item.get("meaning", "")))
            rows += (
                '<div style="display:flex; gap:10px; align-items:baseline;'
                ' padding:6px 0; border-bottom:1px solid rgba(139,148,158,0.15);">'
                f'<code style="font-family:\'Courier New\',monospace; font-size:13px;'
                f' color:#2dd4bf; background:rgba(45,212,191,0.12);'
                f' border:1px solid rgba(45,212,191,0.35); border-radius:6px;'
                f' padding:2px 8px; white-space:nowrap;">{part}</code>'
                f'<span style="font-size:14px;">{meaning}</span>'
                '</div>'
            )
        st.markdown('<div>' + rows + '</div>', unsafe_allow_html=True)

        # 3) Test results - only if the user entered any test strings.
        test_strings = [ln for ln in test_input.splitlines() if ln.strip()]
        if test_strings:
            st.markdown("##### Test results")
            checks = logic.test_regex(result["pattern"], test_strings)
            cards = ""
            for check in checks:
                if check.get("error"):
                    cards += (
                        '<div style="background:rgba(248,81,73,0.13);'
                        ' border-left:4px solid #f85149; border-radius:8px;'
                        ' padding:10px 14px; margin-bottom:8px; color:#f85149;'
                        ' font-size:13px;">'
                        + html.escape(check["error"]) + '</div>'
                    )
                else:
                    cards += result_card(check["text"], check["matches"])
            st.markdown('<div>' + cards + '</div>', unsafe_allow_html=True)