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

### ⚠️ Notes on Test Failures in Task #2 (Expected QA Findings)

The API sync automation tests (test_urgent_sync.py and test_merge_sync.py) are implemented strictly according to the assignment specification.

When executed against the provided Gmail inbox and Droxi Trello board, the automation intentionally reported several mismatches.
These reflect inconsistencies in the demo data, not issues in the tests.

### 🔍 Merge Behavior Mismatches

According to spec:

Emails with the same subject but different bodies must appear in Trello as
one card whose description contains all bodies (combined).

The following subjects violate this rule:

Subject (Email) Expected Actual Trello Card Description
Task: Baking secrets Should contain both bodies (e.g., "New secret everyday" and "Do not miss it") Only contains "New secret everyday"
Task: Create automation tests Should contain merged multi-line body Trello description does not contain the combined body

These failures were detected automatically by test_merge_sync.py.

### 🔍 Urgent Label Mismatch

Spec:

If the email body contains the word Urgent, the Trello card must have the Urgent label.

The following case violated this rule:

Subject Expected Actual
Task: Have a great year Should have "Urgent" label Card only has "New"

Detected by test_urgent_sync.py.

### 🧭 Interpretation

These failures indicate:

The test logic is correct, aligned with the assignment requirements.

The sample Gmail/Trello environment does not fully reflect the described synchronization logic.

The automation effectively identifies these discrepancies — which is what a QA engineer is expected to do.

This is intentional and documented as part of Task #2’s expected analysis.

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
