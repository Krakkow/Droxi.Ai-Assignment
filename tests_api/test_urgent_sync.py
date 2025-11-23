"""

Task #2 - Part 1:
Each mail that its body contains the word “Urgent” should appear
as a card in Trello with “Urgent” label.
"""

import pytest
from api.helpers import normalize_subject_for_trello


def _build_cards_by_title(cards: list[dict]) -> dict[str, list[dict]]:
    """
    Groups cards by their title.
    returns: { title: [card1, card2, ...], ... }
    """
    result: dict[str, list[dict]] = {}

    for card in cards:
        title = (card.get("name") or "").strip()
        if not title:
            continue
        if title not in result:
            result[title] = []
        result[title].append(card)
    
    return result

def _card_has_urgent_label(card: dict) -> bool:
    labels = card.get("labels", []) or []
    for label in labels:
        if label.get("name") == "Urgent":
            return True
    return False

def _any_card_has_urgent_label(cards: list[dict]) -> bool:
    return any(_card_has_urgent_label(card) for card in cards)

def test_urgent_emails_have_urgent_label(gmail_client, trello_client):
    """
    For every gmail email that its body contains 'urgent', there should be
    at leset one Trello card with the same title and an 'Urgent' label.
    """

    # Fetch data from both gmail and Trello
    urgent_emails = gmail_client.get_urgent_emails(max_results=50)
    trello_cards = trello_client.get_board_cards()

    # If there are no urgent emails, we skip this test instead of failing it.
    if not urgent_emails:
        pytest.skip("No urgent emails found in inbox.")
    
    # Groups cards by title for easier lookup
    cards_by_title = _build_cards_by_title(trello_cards)

    problems: list[str] = []

    for email in urgent_emails:
        raw_subject = email["subject"] or ""

        if not raw_subject.lower().startswith("task:"):
            continue # Only Task emails participate in Trello sync
        subject = normalize_subject_for_trello(raw_subject)

        # Find cards with matching title
        matching_cards = cards_by_title.get(subject, [])
        if not matching_cards:
            problems.append(
                f"Urgent email with subject '{subject}' has no matching Trello cards."
            )
            continue

        # Check if at least one of the matching cards has "Urgent" label
        if not _any_card_has_urgent_label(matching_cards):
            problems.append(
                f"Trello cards for urgent email subject '{subject}' do not have 'Urgent' label."
            )

    # if problems list is empty, test passes
    # if not, we fail the test with all the problems found
    assert not problems, "Urgent sync validation failed:\n" + "\n".join(f"- {p}" for p in problems)

