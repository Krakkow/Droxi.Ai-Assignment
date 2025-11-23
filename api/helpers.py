"""
Shared helper functions for API sync tests.
"""

def normalize_subject_for_trello(subject: str) -> str:
    """
    Convert an email subject to the expected Trello card title.

    According to spec:
    - If subject starts with 'Task:', remove that prefix.
    - Otherwise use the subject as-is.
    """
    if not subject:
        return ""

    subject = subject.strip()

    if subject.lower().startswith("task:"):
        return subject[5:].strip()

    return subject