import pytest
from playwright.sync_api import Page
from ui.pages.trello_board_page import TrelloBoardPage, CardInfo

EXPECTED_MEETING_TITLE = "summarize the meeting"
EXPECTED_MEETING_DESCRIPTION = "For all of us Please do so"
EXPECTED_MEETING_STATUS = "To Do"
EXPECTED_MEETING_LABEL = "New"


@pytest.mark.ui
def test_summarize_meeting_card(page: Page) -> None:
    """
    Scenario 2: Specific Card Validation ('summarize the meeting')
    """
    board = TrelloBoardPage(page)

    board.log.info("=== Scenario 2: 'summarize the meeting' card validation ===")
    board.open_board()

    card: CardInfo = board.get_card_info(EXPECTED_MEETING_TITLE)

    board.log.info(
        f"Card info retrieved: title='{card.title}', "
        f"status='{card.status}', labels={card.labels}, "
        f"description='{card.description}'"
    )

    # Title matches exactly
    assert card.title == EXPECTED_MEETING_TITLE, (
        f"Card title mismatch. Expected '{EXPECTED_MEETING_TITLE}', got '{card.title}'"
    )

    assert card.description == EXPECTED_MEETING_DESCRIPTION, (
        f"Card description mismatch. Expected '{EXPECTED_MEETING_DESCRIPTION}', "
        f"got '{card.description}'"
    )

    # "New" label is present
    assert EXPECTED_MEETING_LABEL in card.labels, (
        f"Expected label '{EXPECTED_MEETING_LABEL}' to be present. "
        f"Got labels: {card.labels}"
    )

    # Status is "To Do"
    assert card.status == EXPECTED_MEETING_STATUS, (
        f"Card status mismatch. Expected '{EXPECTED_MEETING_STATUS}', got '{card.status}'"
    )
