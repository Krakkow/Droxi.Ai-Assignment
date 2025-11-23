"""
Task #2 - Part 2:
Merging behavior: emails with the same subject (different body)
should appear as a single Trello card whose description contains all bodies.
"""

import pytest
from api.helpers import normalize_subject_for_trello

def _build_card_description_by_title(cards: list[dict]) -> dict[str, str]:
    """
    build a mapping from card title to its dexcription.
    if multiple cards somehow share the same title, we keep the first one.
    """

    result: dict[str, str] = {}

    for card in cards:
        title = (card.get("name") or "").strip()
        desc = card.get("desc", "") or ""
        if title and title not in result:
            result[title] = desc
    return result

def test_merge_same_subject_different_body(gmail_client, trello_client):
    """
    For subjects that appear in more than one email with different bodies,
    Trello should have a single card whose description includes all bodies.
    """

    grouped = gmail_client.get_emails_grouped_by_subject(max_results=100)

    # Only consider Task emails for this system
    task_only_grouped = {
        subject: bodies
        for subject, bodies in grouped.items()
        if subject.lower().startswith("task:")
    }

    # Only keep subjects that have more than one body -> merging scenario
    merge_candidates = {
        subject: bodies
        for subject, bodies in task_only_grouped.items()
        if len(bodies) > 1
    }

    if not merge_candidates:
        pytest.skip("No merge candidates found in inbox (Task: with multiple bodies).")

    trello_cards = trello_client.get_board_cards()
    desc_by_title = _build_card_description_by_title(trello_cards)

    problems: list[str] = []

    for raw_subject, bodies in merge_candidates.items():
        card_title = normalize_subject_for_trello(raw_subject)

        # Look for Trello card whose title matches the normalized subject
        card_desc = desc_by_title.get(card_title)
        if card_desc is None:
            problems.append(
                f"Emails with subject '{raw_subject}' (normalized '{card_title}') "
                f"have no matching Trello card."
            )
            continue

        # For each email body, check that it's present in the card description
        for body in bodies:
            if body not in card_desc:
                problems.append(
                    f"For subject '{raw_subject}' (normalized '{card_title}'), "
                    f"body '{body}' was not found in Trello card description"
                )

    assert not problems, "Merge sync problems:\n" + "\n".join(problems)