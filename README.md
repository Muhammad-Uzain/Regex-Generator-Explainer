# Regex Generator & Explainer

An AI-powered web app that turns a plain-English description into a
regular expression, explains each part of the pattern, and tests it
against sample strings. Built with Python, Streamlit, and Google Gemini.

## Requirements
- Python 3.10 or newer
- A free Google Gemini API key (https://aistudio.google.com)

## Setup
1. Download this folder.
2. Create and activate a virtual environment:
     Windows:      python -m venv venv   then   venv\Scripts\activate
     macOS/Linux:  python3 -m venv venv  then   source venv/bin/activate
3. Install packages:   pip install -r requirements.txt
4. Copy .env.example to a new file named .env and paste your key:
     GEMINI_API_KEY=your_real_key_here

## Run
     streamlit run app.py
Your browser opens the app automatically.

## Notes
- The key is read from .env and never written in the code.
- .env is listed in .gitignore so it is never pushed to GitHub.
