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

## 🌐 End-to-End Scenarios (Gmail ↔ Trello)

1. Basic New Email → New Trello Card (Happy Flow)
   Send a single simple email → verify one card is created in “To Do” with label “New”, correct title from subject, and description from body.

2. Email With “Task:” Prefix in Subject
   Send an email with subject starting with Task: ... → verify Trello card title uses the subject after Task: and not the raw full subject.

3. Email Body With the Word “Urgent” (Label Assignment)
   Send an email whose body contains the word “Urgent” → verify Trello card has both “New” and “Urgent” labels, correct title and description.

4. Two Identical Emails (No Duplications Rule)
   Send two emails with the same subject and same body → verify only one card appears on the Trello board (no duplicate cards created).

5. Merging Different Bodies Under Same Subject
   Send multiple emails with the same subject and different bodies → verify a single Trello card is created where the description concatenates all bodies in order, each on a new line.

6. Move Card to “In Progress” → Gmail Inbox Still Intact
   Take an existing card in “To Do”, drag it to “In Progress” → verify the corresponding Gmail email is still in the inbox (not moved to trash).

7. Move Card to “Done” → Gmail Email Goes to Trash
   Take an existing card in “To Do” or “In Progress”, drag it to “Done” → verify the corresponding Gmail email is now in the Gmail trash folder.

8. Email Without “Urgent” → No Urgent Label
   Send a normal email with no “Urgent” in the body → verify the created Trello card does not have the “Urgent” label (only “New”).

9. Multiple Urgent Emails With Same Subject (Merge + Urgency)
   Send several emails with the same subject, all containing “Urgent” somewhere in the body → verify a single Trello card is created with “Urgent” label and a merged multi-line description.

10. Deletion / Archive in Gmail Does Not Create New Cards
    Delete or archive an existing email in Gmail without moving any card → verify no new Trello cards are created and no existing ones are duplicated.

11. End-to-End Sync Latency / Ordering Check
    Send multiple emails in quick succession with different subjects → verify all cards are eventually created in Trello with correct mapping to inbox emails and ordering is consistent/traceable.

## 🔧 Component-Level / Logic-Level Scenarios

# A. Email → Card Mapping & Content

1. Subject Parsing With and Without “Task:”
   Verify the logic for extracting the card title from email subject with cases: with Task:, without it, mixed capitalization (task:), and subject with only Task: and no text.

2. Description Mapping From Body (Multi-line Support)
   Verify that line breaks in the email body are preserved in the Trello description when they are not part of a merge (single email case).

3. HTML vs Plain Text Body Handling
   Send HTML formatted emails (links, bold, lists) → verify how the description appears in Trello (sanitized text / preserved / broken) and that core text content is still correct.

4. Long Subject and Long Body Handling
   Send an email with very long subject and body → verify the card title and description are not truncated in a way that breaks business logic.

# B. Label Logic (“New” and “Urgent”)

1. New Card Always Has “New” Label
   For multiple types of emails (with/without urgent, short/long), verify every newly created card always gets the “New” label.

2. Urgent Detection – True Positive
   Email body contains “Urgent” as a clear word → verify the “Urgent” label is added to the card.

3. Urgent False Positive: Part of Another Word
   Email body contains strings like “insurgent”, “urgently”, or “URGENTLY” → decide and verify if the logic treats these as “Urgent” or not (word-boundary behavior).

4. Urgent Case Sensitivity
   Test “urgent”, “URGENT”, “Urgent”, “uRgEnT” → verify whether detection is case-insensitive as expected.

# C. Merging & Deduplication Logic

1. Deduplication True Positive (Exact Same Subject + Body)
   Verify that duplicate emails (identical subject and body) produce only one card even if many duplicates arrive later.

2. Deduplication False Negative (Minor Body Difference)
   Two emails with same subject but only a small change in the body (extra whitespace, trailing space) → verify if they’re treated as duplicates or as separate entries to be merged.

3. Merging Order of Bodies
   Send emails in a specific order (Mail1, Mail2, Mail3) with same subject and different bodies → verify the Trello description merges them in the correct chronological order.

4. Merging After a Card Already Exists
   First send an email that creates a card, then later send more emails with the same subject → verify the existing card is updated (description extended) rather than creating new cards.

# D. Gmail State vs Trello Column State

1. Inbox ↔ “To Do” / “In Progress” Mapping
   Verify that as long as the email remains in inbox, the card is not moved automatically to “Done” or removed.

1. Trash ↔ “Done” Mapping Consistency
   Move an email manually to Trash in Gmail → verify if the system either moves the matched card to “Done” or keeps Trello unchanged (define expected behavior and test against it).

1. No Orphan Cards (Trello Without Gmail Match)
   Check that every card in “To Do” and “In Progress” has a matching email in inbox, and every card in “Done” has a matching email in trash; any orphan card is a defect.

# E. Negative / Error / Robustness Scenarios

1. Email Without Subject
   Send an email with an empty subject → verify how the system sets the Trello card title (empty, “(no subject)”, or error) and check that behavior is consistent.

2. Email Without Body
   Send an email with subject but empty body → verify the Trello card description is empty and that no merge issues occur when future emails arrive with same subject.

3. Unsupported / Non-Text Attachments Only
   Send an email with only attachments and no body → verify that the card is still created (or not) and that description doesn’t break.

4. Malformed / Very Large Emails
   Simulate or conceptualize oversized or malformed emails → verify system behavior (does it skip, partially sync, or error gracefully).

5. System Offline / API Failure Simulation
   Imagine Trello or Gmail APIs failing temporarily → describe how you’d verify retries, error logs, and that no partial/duplicate cards are created once the service recovers.

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

This project includes a full UI automation suite built with Python, Playwright, and the Page Object Model (POM) design pattern.

## 📄 Implemented Scenarios

Scenario 1 – Urgent Cards Validation

Automatically validates all cards across the entire Trello board that have an “Urgent” label.
For each urgent card, the test extracts and verifies:

- Card title

- Card description

- Card labels

- Column/status (To Do, In Progress, Done)

Scenario 2 – “summarize the meeting” Card Validation

Locates the “summarize the meeting” card and performs full validation of:

- Exact card title

- Exact card description

- Required label(s) (e.g., “New”)

- Correct column (“To Do”)

The test opens the card modal, extracts required fields from the UI, validates them, and closes the modal cleanly.

## ▶️ How to Run the UI Tests

## 1️⃣ Install Dependencies

Inside the project root:

```bash
pip install -r requirements.txt (this is something you already did to run the api tests)
```

## 2️⃣ Install Playwright browsers

```bash
playwright install
```

## 3️⃣ Generate Trello Authentication State (first-time only)

To run tests without manually logging in each time, Playwright uses
trello_auth_state.json as a stored login session.
Run:

```bash
python auth_setup.py
```

A browser will open — log into the Trello board using the provided credentials.
The session will be saved automatically.

The file is ignored by Git for security.

## 4️⃣ Run All UI Tests

```bash
pytest ui/tests_ui --headed -vv
```

You can also run headless:

```bash
pytest ui/tests_ui -vv
```

## 5️⃣ Run a Specific Scenario

Scenario 1 - Urgent Cards Validation

```bash
pytest ui/tests_ui/test_trello_urgent_cards.py --headed -vv

```

Scenario 2 - "Summerize the meeting" card

```bash
pytest ui/tests/test_trello_summarize_meeting.py --headed -vv
```

## 6️⃣ Log Output

Logging is enabled via pytest.ini
To disable log capturing temprarily:

```bash
pytest -s -vv
```

## ✔ Final Notes

Project is modular and extendable.

Credentials are secured via .gitignore.

All tests execute via pytest.

The solution follows clean code and POM design practices.

```

```
