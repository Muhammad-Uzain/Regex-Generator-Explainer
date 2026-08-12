# Regex Generator & Explainer

An AI-powered web app that turns a plain-English description into a working
**regular expression**, explains each part of the pattern in simple terms, and
then **tests that pattern against your own sample strings** to prove it actually
works.

Built with **Python**, **Streamlit**, and the **Google Gemini API**.

> Type something like *"an email address"* and the app gives you a regex, a
> part-by-part explanation, and a live match/no-match check against your test
> strings.

---

## Table of contents

- [Regex Generator \& Explainer](#regex-generator--explainer)
  - [Table of contents](#table-of-contents)
  - [What it does](#what-it-does)
  - [How it works](#how-it-works)
  - [Prerequisites](#prerequisites)
  - [Project structure](#project-structure)
  - [Setup (step by step)](#setup-step-by-step)
    - [1. Get the code](#1-get-the-code)
    - [2. Create a virtual environment](#2-create-a-virtual-environment)
    - [3. Activate the virtual environment](#3-activate-the-virtual-environment)
    - [4. Install the dependencies](#4-install-the-dependencies)
    - [5. Add your Gemini API key](#5-add-your-gemini-api-key)
  - [Running the app](#running-the-app)
  - [Coming back later (every new session)](#coming-back-later-every-new-session)
  - [Building the UI without a key (mock mode)](#building-the-ui-without-a-key-mock-mode)
  - [Test cases](#test-cases)
  - [Troubleshooting](#troubleshooting)
  - [Security notes](#security-notes)
  - [Team](#team)

---

## What it does

- Accepts a plain-English description of a text pattern (e.g. "a phone number").
- Sends it to Google's Gemini AI, which returns a regular expression plus an
  explanation of each part.
- Tests the generated pattern against sample strings you provide and shows which
  ones match and which do not.
- Validates your input and handles errors gracefully, so the app never crashes
  in front of the user.

## How it works

The interesting idea behind this project: **AI models can be confidently wrong,
so we don't just trust the output — we verify it.** The AI generates a pattern,
and then the app runs that pattern against real test strings using Python's
built-in `re` module. The match/no-match results are your proof the pattern is
correct, independent of what the AI claimed.

The code is split into two clear layers so the team could work in parallel:

- **The interface** (`app.py`) — everything the user sees, built with Streamlit.
- **The engine** (`regex_logic.py`) — the Gemini API call and the regex testing.

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.10 or newer.** Check your version with:
  ```bash
  python --version
  ```
  > Note: very new releases (e.g. Python 3.14) can occasionally be ahead of what
  > some packages support. If installation fails later, Python **3.12** is a safe,
  > well-supported choice.

- **A free Google Gemini API key.** Get one at
  [https://aistudio.google.com](https://aistudio.google.com) → **Get API key** →
  **Create API key**. No credit card is required.

- **Git** (only needed if you are cloning the repository).

---

## Project structure

```text
regex-generator/
├── app.py              # The Streamlit user interface (run this file)
├── regex_logic.py      # The engine: Gemini API call + regex testing
├── mock_logic.py       # A fake engine for building the UI without a key
├── requirements.txt    # The list of packages to install
├── .env                # YOUR real API key — stays local, never committed
├── .env.example        # A template showing what .env should contain
├── .gitignore          # Keeps .env and the venv out of the repository
└── README.md           # This file
```

| File | Purpose |
|------|---------|
| `app.py` | The web app. Draws the page, takes input, shows results. |
| `regex_logic.py` | Calls Gemini, parses the response, tests the pattern. |
| `mock_logic.py` | Returns fake data instantly, so the UI can be built with no key. |
| `requirements.txt` | Everything `pip` needs to install. |
| `.env` | Holds your personal `GEMINI_API_KEY`. **Never pushed to GitHub.** |
| `.env.example` | Safe template (no real key) so others know what is needed. |
| `.gitignore` | Tells Git to ignore `.env`, the `venv` folder, and cache files. |

---

## Setup (step by step)

These steps take you from nothing to a running app. Do them in order, in a
terminal, **from inside the project folder**.

### 1. Get the code

If the project is on GitHub, clone it and move into the folder:

```bash
git clone https://github.com/<your-group>/<repo-name>.git
cd <repo-name>
```

If you already have the folder, just open a terminal inside it.

### 2. Create a virtual environment

A **virtual environment** (venv) is a private, isolated space that holds this
project's packages, separate from the rest of your computer. This prevents
version clashes between projects and is standard practice for Python.

Create it once with:

```bash
python -m venv venv
```

This creates a new folder called `venv` inside your project. You only need to do
this **once** per project — not every time.

> The `venv` folder is listed in `.gitignore`, so it will **not** be pushed to
> GitHub. That is intentional: each person creates their own locally.

### 3. Activate the virtual environment

Creating the venv is not enough — you have to **activate** it so your terminal
uses the project's isolated Python instead of the system one. The command depends
on your operating system and terminal:

**Windows — Git Bash:**
```bash
source venv/Scripts/activate
```

**Windows — PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Windows — Command Prompt (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

**How do you know it worked?** Your terminal prompt will change to show `(venv)`
at the start of the line, like this:

```text
(venv) user@computer MINGW64 ~/regex-generator
```

That `(venv)` is your confirmation that the environment is active.

> ### IMPORTANT — you must activate the venv EVERY new session
>
> Activation only lasts for the **current terminal window**. The moment you:
> - close the terminal, or
> - open a new terminal / new VS Code window, or
> - restart your computer,
>
> ...the environment is **no longer active**, even though it still exists on disk.
> You do **not** reinstall anything — you just **activate it again** with the same
> command from step 3 before you run the app.
>
> If you ever open a fresh terminal and see an error like
> `streamlit: command not found` or `No module named 'streamlit'`, the cause is
> almost always that you **forgot to activate the venv**. Run the activate command
> and try again.

To leave the environment when you are finished, type:

```bash
deactivate
```

### 4. Install the dependencies

With the venv **active** (you should see `(venv)`), install everything the
project needs in one command:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — the web app framework
- `google-genai` — the official Google Gemini SDK
- `python-dotenv` — loads your API key from the `.env` file

This may take a minute and print many lines. If it ends with a notice about
upgrading `pip`, you can safely ignore it. You only need to install **once** per
venv (unless `requirements.txt` changes).

Confirm Streamlit installed correctly:

```bash
streamlit version
```

If that prints a version number, you are good. If it says "command not found",
use `python -m streamlit version` instead, and double-check the venv is active.

### 5. Add your Gemini API key

The app reads your key from a file named `.env`. This keeps the secret out of the
code and out of GitHub.

1. Copy the template to a new file called `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` in your editor and replace the placeholder with your real key:
   ```text
   GEMINI_API_KEY=your_real_key_here
   ```
   Paste the key immediately after the `=` with **no spaces** before or after it.
   A stray space is the most common reason a key "doesn't work".

> Each team member uses their **own** key in their **own** local `.env`. Keys are
> personal (tied to your Google account and your free quota), so they are never
> shared through the repository.

---

## Running the app

With the venv active and your key in `.env`, start the app from the project
folder:

```bash
streamlit run app.py
```

Your browser will open automatically at **`http://localhost:8501`**. Type a
description (for example, "an email address"), optionally add some test strings
(one per line), and click **Generate regex**.

**To stop the app**, return to the terminal and press:

```text
Ctrl + C
```

> If `streamlit run app.py` says the command is not found, either the venv is not
> active (re-run the activate command) or use `python -m streamlit run app.py`.

---

## Coming back later (every new session)

Once everything is set up, **you do not repeat the whole installation**. When you
sit down to work on the project in a fresh terminal, you only need three steps:

```bash
# 1. Go into the project folder
cd path/to/regex-generator

# 2. Activate the virtual environment (see step 3 for your OS)
source venv/Scripts/activate      # Windows Git Bash example

# 3. Run the app
streamlit run app.py
```

That's it. Creating the venv and installing packages were one-time steps;
**activating** is the only part you repeat each session.

---

## Building the UI without a key (mock mode)

You can run and build the **entire interface with no API key and no internet**,
using the included fake engine (`mock_logic.py`). This is useful for working on
the UI while the real engine is still being finished.

At the top of `app.py`, switch which line is commented so the **mock** is active:

```python
# import regex_logic as logic     # real engine (needs a key)
import mock_logic as logic         # fake engine (no key needed)
```

Then run `streamlit run app.py` as usual. The app works end to end, but always
returns the same email example regardless of what you type — that is expected, it
is fake data for building the UI.

> **Before you demo or submit the project, switch back to the real engine:**
> ```python
> import regex_logic as logic       # real engine (needs a key)
> # import mock_logic as logic      # fake engine (no key needed)
> ```
> Otherwise the app will only ever return the canned email pattern.

---

## Test cases

The app is checked against three cases. Because the AI's exact output varies
slightly each run, success is judged by **behaviour** (does it match the right
strings?), not by the exact pattern text.

| # | Description entered | Should match | Should NOT match |
|---|---------------------|--------------|------------------|
| 1 | an email address | `john@example.com` | `not-an-email` |
| 2 | a phone number like 123-456-7890 | `123-456-7890` | `1234567890` |
| 3 | a date like 31/12/2025 | `31/12/2025` | `2025-12-31` |

---

## Troubleshooting

| Problem | Likely cause and fix |
|---------|----------------------|
| `streamlit: command not found` | The venv is not active. Run the activate command, or use `python -m streamlit run app.py`. |
| `No module named 'streamlit'` / `'google'` / `'dotenv'` | Packages not installed in the active environment. Confirm `(venv)` is showing, then `pip install -r requirements.txt`. |
| `No API key found` | `.env` is missing, misnamed, or in the wrong folder. It must be named exactly `.env` and sit next to `app.py`. |
| `API key not valid` / `403 PERMISSION_DENIED` | The key was pasted with a stray space or is incomplete. Recopy it from AI Studio. |
| `404` / model not found | The model name changed. Check the current models in Google AI Studio and update `MODEL_NAME` in `regex_logic.py`. |
| `429 RESOURCE_EXHAUSTED` | You hit the free-tier rate limit. Wait a minute and try again. |
| App only returns the same email pattern | `app.py` is still importing `mock_logic`. Switch it to `regex_logic`. |
| `pip install` fails with build errors | Your Python may be too new for some packages. Try Python 3.12 and recreate the venv. |

---

## Security notes

- The API key lives only in your local `.env` file and is **never committed**.
- `.gitignore` ignores `.env`, so it stays out of the repository.
- Only `.env.example` (a placeholder with no real key) is committed, as a guide.
- After adding a real key, you can confirm it is safe with `git status` — `.env`
  should **not** appear in the list of changes.

---

## Team

**Course:** Implementing GEN AI Tools in Python — Group Project

| Name | Student ID | Role |
|------|-----------|------|
| Muhammad Uzain | 100385184 | Back-end / engine (API + logic) |
| Chetanbir Singh | 100442356 | Back-end / engine (API + logic) |
| Sarthak Narang | 100446252 | Front-end / UI |
| Sepher Zolfaghari | 100423483 | Front-end / UI |

**API used:** Google Gemini (free tier) &nbsp;|&nbsp; **Framework:** Streamlit