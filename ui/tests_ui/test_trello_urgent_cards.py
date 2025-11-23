import pytest
from playwright.sync_api import Page
from ui.pages.trello_board_page import TrelloBoardPage, CardInfo

VALID_STATUSES = ["To Do", "In Progress", "Done"]


@pytest.mark.ui
def test_urgent_cards_validation(page: Page) -> None:
    """
    Scenario 1: Urgent Cards Validation

    1. Login to Trello
    2. Find all cards with 'Urgent' label across all columns
    3. For each urgent card, extract:
       - Card title
       - Card description
       - Labels
       - Current status (To Do, In Progress, Done)
    """
    board = TrelloBoardPage(page)

    # login_to_trello(page)

    board.log.info("=== Scenario 1: Urgent Cards Validation ===")
    board.open_board()

    urgent_cards: list[CardInfo] = board.get_urgent_cards_info()
    board.log.info(f"Found {len(urgent_cards)} urgent cards")

    assert urgent_cards, "Expected at least one 'Urgent' card on the board."

    for card in urgent_cards:
        board.log.info(
            f"Validating urgent card: title='{card.title}', "
            f"status='{card.status}', labels={card.labels}"
        )

        # Title should not be empty
        assert card.title, "Urgent card should have a non-empty title."

        # Description should not be empty
        assert card.description, f"Urgent card '{card.title}' should have a description."

        # Must include 'Urgent' label
        assert "Urgent" in card.labels, (
            f"Urgent card '{card.title}' should include 'Urgent' label. "
            f"Got labels: {card.labels}"
        )

        # Status must be one of the known columns
        assert card.status in VALID_STATUSES, (
            f"Urgent card '{card.title}' has unexpected status '{card.status}'. "
            f"Expected one of {VALID_STATUSES}"
        )
