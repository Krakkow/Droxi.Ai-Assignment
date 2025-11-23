# Droxi.ai – QA Automation Assignment

This repository contains the full solution for the Droxi.ai QA Automation assignment, including:

- **Task #1:** Manual test descriptions (in this README).
- **Task #2:** API sync validation between Gmail inbox and Trello board.
- **Task #3:** UI automation using Python + Playwright + Page Object Model.

The project is written in **Python 3.14** and uses **pytest**, **Playwright**, and Google/Trello APIs.

---

## 📦 Project Structure

qa_automation_assignment/
│
├── api/
│ ├── gmail_client.py
│ ├── trello_client.py
│
├── tests_api/
│ ├── conftest.py
│ ├── test_urgent_sync.py
│ ├── test_merge_sync.py
│
├── tests_ui/ # Created later for UI automation
│
├── config.py
├── README.md
├── .gitignore

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone <your_repo_url>
cd qa_automation_assignment
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers (for Task #3)

```bash
playwright install
```

## 🔐 Authentication (IMPORTANT)

```bash
Gmail API authentication

Before running Gmail tests, generate a token:

Run:

python main.py

Login with the provided assignment Gmail account.

Approve the permissions.

After seeing “You may close this window”, a token.json file is created.

Note:
token.json and credentials.json are in .gitignore
They must not be committed.

Trello API authentication

Trello API key/token are loaded from config.py:

TRELLO_API_KEY = "..."
TRELLO_API_TOKEN = "..."
TRELLO_BOARD_ID = "2GzdgPlw"

These are already included per the assignment instructions.
```

## 🔒 Environment Variables (.env)

This project uses a `.env` file to store sensitive configuration values such as the Trello API key and token.

A template file is provided:

```sql
.env.example
# Copy this file to .env and replace the values with real credentials
TRELLO_API_KEY=your-key-here
TRELLO_API_TOKEN=your-token-here
```

# 1. Create your real .env file

```bash
cp .env.example .env       # Mac/Linux
copy .env.example .env     # Windows
```

# 2. Edit .env and insert the actual Trello credentials (provided in the assignment).

The .env file is ignored by Git and never uploaded to GitHub.

The project automatically loads .env using:

```python
from dotenv import load_dotenv
load_dotenv()
```

## 🧪 Running Tests

```bash
Run all tests:
pytest -q

Run only API sync tests:
pytest tests_api -q

Run only UI tests (after Task #3):
pytest tests_ui -q
```

## 📝 Task #1 – Manual Testing

Below is a brief outline of the manual testing scenarios:

## 🧪 Task #2 – Automated Sync Validation (API)

Implemented using:

gmail_client.py

trello_client.py

pytest

Tests include:

test_urgent_sync.py

test_merge_sync.py

These compare live Gmail inbox data with live Trello board data.

## 🖥️ Task #3 – UI Automation (Playwright + POM)

Included files:

Page Objects under ui/pages/

Test cases under tests_ui/

Scenarios implemented:

Scenario 1: Urgent Cards Validation

Scenario 2: “summarize the meeting” card validation

## ✔ Final Notes

Project is modular and extendable.

Credentials are secured via .gitignore.

All tests execute via pytest.

The solution follows clean code and POM design practices.
