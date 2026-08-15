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
 
 
st.set_page_config(
    page_title="RegexLab - AI Regex Generator",
    page_icon=":mag:",
    layout="wide",
)
 
LIME = "#a3e635"
 
# ---------- CSS: wider container, spacing, primary button text ----------
st.markdown(
    """
    <style>
      .block-container {padding-top: 3.5rem; padding-bottom: 3rem; max-width: 1400px;}
      div[data-testid="stButton"] button[kind="primary"] {
          color:#0a0a0f !important; font-weight:700 !important;}
      label {font-weight:600 !important;}
    </style>
    """,
    unsafe_allow_html=True,
)
 
 
# ---------- small HTML helpers ----------
def section_header(num, title, subtitle):
    """A numbered section heading like  01  Describe & test."""
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:12px;">'
        f'<span style="font-family:\'Courier New\',monospace; color:{LIME};'
        f' font-weight:700; font-size:13px;">{num}</span>'
        f'<span style="font-size:18px; font-weight:800;">{html.escape(title)}</span></div>'
        f'<div style="color:#8b949e; font-size:13px; margin:2px 0 12px;">'
        f'{html.escape(subtitle)}</div>',
        unsafe_allow_html=True,
    )
 
 
def result_row(text, matched):
    """One colour-coded test-result row (green if matched, red if not)."""
    text = html.escape(text)
    if matched:
        bg, line, accent, icon, label = (
            "rgba(46,160,67,0.15)", "#3fb950", "#3fb950", "&#10003;", "MATCH")
    else:
        bg, line, accent, icon, label = (
            "rgba(248,81,73,0.13)", "#f85149", "#f85149", "&#10007;", "NO MATCH")
    return (
        f'<div style="display:flex; align-items:center; gap:10px; background:{bg};'
        f' border:1px solid {line}55; border-left:4px solid {line}; border-radius:8px;'
        f' padding:10px 14px; margin-bottom:8px;">'
        f'<span style="color:{accent}; font-weight:800;">{icon}</span>'
        f'<span style="font-family:\'Courier New\',monospace; font-size:13px;'
        f' word-break:break-all;">{text}</span>'
        f'<span style="margin-left:auto; color:{accent}; font-size:11px; font-weight:700;'
        f' letter-spacing:.08em;">{label}</span></div>'
    )
 
 
def step_card(num, title, desc):
    """One step in the footer 'How to use' guide."""
    return (
        f'<div style="flex:1 1 220px; min-width:210px; max-width:300px;'
        f' border:1px solid rgba(163,230,53,0.20); border-radius:12px;'
        f' padding:14px 16px; background:rgba(163,230,53,0.03);">'
        f'<div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">'
        f'<span style="display:inline-flex; align-items:center; justify-content:center;'
        f' width:24px; height:24px; border-radius:50%; background:{LIME}; color:#0a0a0f;'
        f' font-weight:800; font-size:13px;">{num}</span>'
        f'<span style="font-weight:700; font-size:14px;">{html.escape(title)}</span></div>'
        f'<div style="color:#8b949e; font-size:12.5px; line-height:1.5;">'
        f'{html.escape(desc)}</div></div>'
    )
 
 
# ---------- header + hero + description (full width) ----------
ready = getattr(logic, "client", None) is not None
if ready:
    badge = (
        f'<span style="border:1px solid rgba(163,230,53,0.45); color:{LIME};'
        f' border-radius:20px; padding:4px 12px; font-size:12px; white-space:nowrap;">'
        f'&#9679;&nbsp;Gemini ready</span>'
    )
else:
    badge = (
        '<span style="border:1px solid rgba(248,81,73,0.45); color:#f85149;'
        ' border-radius:20px; padding:4px 12px; font-size:12px; white-space:nowrap;">'
        '&#9679;&nbsp;Key missing</span>'
    )
 
st.markdown(
    f'''
    <div style="display:flex; align-items:center; justify-content:space-between;
                gap:12px; margin-bottom:6px;">
      <div style="display:flex; align-items:center; gap:12px;">
        <div style="font-family:'Courier New',monospace; font-size:20px; font-weight:800;
                    color:#0a0a0f; background:{LIME}; border-radius:12px;
                    padding:4px 12px;">.*</div>
        <div>
          <div style="font-size:22px; font-weight:800; line-height:1.1;">RegexLab</div>
          <div style="color:#8b949e; font-size:13px;">AI Pattern Studio</div>
        </div>
      </div>
      {badge}
    </div>
    <div style="text-align:center; margin:14px 0 18px;">
      <div style="font-family:'Courier New',monospace; color:{LIME}; letter-spacing:.22em;
                  font-size:12px; margin-bottom:6px;">GENERATIVE AI &bull; REGEX &bull; TESTING</div>
      <div style="font-size:26px; font-weight:800; line-height:1.15;">
        Describe the pattern. <span style="color:#8b949e;">We build the regex.</span>
      </div>
      <div style="color:#8b949e; font-size:14px; line-height:1.6; max-width:640px;
                  margin:12px auto 0;">
        Turn plain English into a working regular expression. Describe what you want to
        match, add a few sample strings, and RegexLab generates the pattern, explains
        every part, and verifies it live with Python &mdash; powered by Google Gemini.
      </div>
    </div>
    <hr style="border:none; border-top:1px solid rgba(163,230,53,0.25); margin:0 0 20px;">
    ''',
    unsafe_allow_html=True,
)
 
 
# ---------- session state ----------
if "result" not in st.session_state:
    st.session_state.result = None
if "desc" not in st.session_state:
    st.session_state.desc = ""
if "tests" not in st.session_state:
    st.session_state.tests = ""
 
# Quick-start presets: label -> (description, simple sample test strings).
# Each sample has one string that should match and one that should not.
PRESETS = {
    "Email":  ("an email address",                "john@example.com\nnot-an-email"),
    "Date":   ("a date in DD/MM/YYYY format",      "31/12/2025\n2025-12-31"),
    "Postal": ("a Canadian postal code",           "K1A 0B1\n12345"),
    "Phone":  ("a phone number like 123-456-7890", "123-456-7890\n1234567890"),
}
 
 
# ---------- callbacks (run before the widgets are drawn) ----------
def apply_preset(desc_value, tests_value):
    st.session_state.desc = desc_value      # fill the description
    st.session_state.tests = tests_value    # fill the sample test strings
    st.session_state.result = None          # clear any old result
 
def clear_inputs():
    st.session_state.desc = ""
    st.session_state.tests = ""
    st.session_state.result = None
 
 
# ================= two columns: inputs (left) | results (right) =================
col_input, col_output = st.columns([1, 1.2], gap="large")
 
# ===== LEFT: 01 - Describe & test =====
with col_input:
    with st.container(border=True):
        section_header("01", "Describe & test",
                       "Pick a preset to auto-fill an example, or write your own.")
 
        st.caption("Quick start")
        preset_items = list(PRESETS.items())
        for i in range(0, len(preset_items), 2):        # 2 buttons per row
            c1, c2 = st.columns(2)
            for (label, (dval, tval)), col in zip(preset_items[i:i + 2], [c1, c2]):
                col.button(label, use_container_width=True,
                           on_click=apply_preset, args=(dval, tval))
 
        description = st.text_input(
            "What should the regex match?",
            key="desc",
            placeholder="e.g. an email address",
        )
        test_input = st.text_area(
            "Test strings - one per line",
            key="tests",
            placeholder="john@example.com\nnot-an-email\nhello@world.co",
            height=150,
        )
 
        opt_left, opt_right = st.columns([1.4, 1])
        with opt_left:
            match_mode = st.selectbox(
                "Match mode",
                ["Find inside text", "Full string only"],
                help="Find inside text: matches anywhere in the string. "
                     "Full string only: the whole string must match.",
            )
        with opt_right:
            ignore_case = st.toggle("Ignore case", value=False)
 
        gen_col, clr_col = st.columns([3, 1])
        with gen_col:
            generate_clicked = st.button(
                "Generate Regex", type="primary", use_container_width=True
            )
        with clr_col:
            st.button("Clear", use_container_width=True, on_click=clear_inputs)
 
        if generate_clicked:
            if not description.strip():
                st.warning("Please describe what you want to match first.")
            else:
                with st.spinner("Asking Gemini..."):
                    st.session_state.result = logic.generate_regex(description)
 
# ===== RIGHT: results =====
with col_output:
    result = st.session_state.result
 
    if result is None:
        with st.container(border=True):
            st.markdown(
                f'<div style="text-align:center; color:#8b949e; padding:56px 10px;">'
                f'<div style="font-family:\'Courier New\',monospace; font-size:30px;'
                f' color:{LIME}; margin-bottom:8px;">{{ }}</div>'
                'Your regex, explanation, and test results will appear here.</div>',
                unsafe_allow_html=True,
            )
 
    elif not result["success"]:
        with st.container(border=True):
            st.markdown(
                f'<div style="background:rgba(248,81,73,0.13); border-left:4px solid #f85149;'
                f' border-radius:8px; padding:14px 16px; color:#f85149;">'
                f'<b>Error:</b> {html.escape(result["error"])}</div>',
                unsafe_allow_html=True,
            )
 
    else:
        # ----- 02 - Generated regex -----
        with st.container(border=True):
            section_header("02", "Generated regex", "The pattern Gemini produced.")
            st.code(result["pattern"], language="text")
 
        # ----- 03 - Explanation -----
        with st.container(border=True):
            section_header("03", "Explanation", "What each part of the pattern does.")
            rows = ""
            for item in result["explanation"]:
                part = html.escape(str(item.get("part", "")))
                meaning = html.escape(str(item.get("meaning", "")))
                rows += (
                    '<div style="display:flex; gap:10px; align-items:baseline; padding:6px 0;'
                    ' border-bottom:1px solid rgba(139,148,158,0.15);">'
                    f'<code style="font-family:\'Courier New\',monospace; font-size:13px;'
                    f' color:{LIME}; background:rgba(163,230,53,0.12);'
                    f' border:1px solid rgba(163,230,53,0.35); border-radius:6px;'
                    f' padding:2px 8px; white-space:nowrap;">{part}</code>'
                    f'<span style="font-size:14px;">{meaning}</span></div>'
                )
            st.markdown('<div>' + rows + '</div>', unsafe_allow_html=True)
 
        # ----- 04 - Test results (uses Match mode + Ignore case) -----
        test_strings = [ln for ln in test_input.splitlines() if ln.strip()]
        if test_strings:
            whole_string = (match_mode == "Full string only")
            checks = logic.test_regex(
                result["pattern"], test_strings,
                ignore_case=ignore_case, whole_string=whole_string,
            )
            matched_count = sum(1 for c in checks if c.get("matches"))
            with st.container(border=True):
                mode_note = "whole-string" if whole_string else "find-inside"
                case_note = ", ignore case" if ignore_case else ""
                section_header(
                    "04", "Test results",
                    f"Python verified these against the pattern "
                    f"({mode_note}{case_note}) - {matched_count}/{len(checks)} matched.",
                )
                cards = ""
                for check in checks:
                    if check.get("error"):
                        cards += (
                            '<div style="background:rgba(248,81,73,0.13);'
                            ' border-left:4px solid #f85149; border-radius:8px;'
                            ' padding:10px 14px; margin-bottom:8px; color:#f85149;'
                            ' font-size:13px;">' + html.escape(check["error"]) + '</div>'
                        )
                    else:
                        cards += result_row(check["text"], check["matches"])
                st.markdown('<div>' + cards + '</div>', unsafe_allow_html=True)
 
 
# ================= footer: how to use =================
st.markdown(
    f'''
    <hr style="border:none; border-top:1px solid rgba(163,230,53,0.25); margin:34px 0 18px;">
    <div style="font-size:16px; font-weight:800; text-align:center; margin-bottom:14px;">
      How to use RegexLab
    </div>
    <div style="display:flex; gap:14px; flex-wrap:wrap; justify-content:center;">
      {step_card("1", "Describe", "Type what you want to match in plain English, or tap a preset chip.")}
      {step_card("2", "Add test strings", "Paste a few example strings, one per line, to check the pattern against.")}
      {step_card("3", "Set options & generate", "Choose the match mode, toggle ignore case if needed, then hit Generate Regex.")}
      {step_card("4", "Review & verify", "Read the pattern and explanation, and see which test strings match (green) or not (red).")}
    </div>
    <div style="text-align:center; color:#6b7280; font-size:12px; margin-top:22px;">
      Powered by Google Gemini &bull; Built with Streamlit
    </div>
    ''',
    unsafe_allow_html=True,
)