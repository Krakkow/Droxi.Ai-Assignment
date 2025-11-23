from dataclasses import dataclass
from playwright.sync_api import Page, Locator
from ui.pages.base_page import BasePage

TRELLO_BOARD_URL = "https://trello.com/b/2GzdgPlw/droxi"

# ----- Selector constants -----
BOARD_HEADER_SELECTOR = '[data-testid="board-name-display"]'
LIST_SELECTOR = '[data-testid="list"]'
LIST_CARD_SELECTOR = '[data-testid="list-card"]'
LIST_NAME_SELECTOR = '[data-testid="list-name"]'
CARD_TITLE_SELECTOR = '[data-testid="card-name"]'
COMPACT_LABEL_SELECTOR = '[data-testid="compact-card-label"]'


@dataclass
class CardInfo:
    """
    This is just a simple data model for a Trello card.
    """
    title: str
    description: str
    labels: list[str]
    status: str  # E.g., "To Do", "In Progress", "Done"


class TrelloBoardPage(BasePage):
    """
    Page Object Model for the Trello Board page.
    """

    PATH = TRELLO_BOARD_URL

    # --- Locators ---
    board_header: Locator
    columns: Locator
    cards: Locator
    card_modal: Locator
    card_modal_title: Locator
    card_modal_description_content: Locator
    card_modal_description_button: Locator
    card_modal_labels: Locator
    card_modal_close_button: Locator

    def __init__(self, page: Page, base_url: str | None = None) -> None:
        super().__init__(page, base_url)

        # Initialize locators
        self.board_header = self.page.locator(BOARD_HEADER_SELECTOR)
        self.columns = self.page.locator(LIST_SELECTOR)
        self.cards = self.page.locator(LIST_CARD_SELECTOR)

        self.card_modal = self.page.locator('[data-testid="card-back-name"]')
        self.card_modal_title = self.page.locator('[data-testid="card-back-title-input"]')
        self.card_modal_description_content = self.page.locator('[data-testid="description-content-area"]')
        self.card_modal_description_button = self.page.locator('[data-testid="description-button"]')
        self.card_modal_labels = self.page.locator('[data-testid="card-label"]')
        self.card_modal_close_button = self.page.locator('[data-testid="CloseIcon"]')

    # ==================================================
    # Public high-level methods
    # ==================================================

    def open_board(self) -> None:
        """
        Opens the Trello board page and waits for board header (title) to be visible.
        """
        self.log.info(f"Opening board using PATH='{self.PATH}'")
        self.open(self.PATH)
        self.board_header.wait_for(state="visible", timeout=10_000)
        self.log.info("Board opened successfully.")

    def get_board_title(self) -> str:
        """
        Returns the title of the Trello board.
        """
        self.log.info("Getting Board Title.")
        return self.board_header.inner_text().strip()

    # ==================================================
    # Private helper methods (small, reusable pieces)
    # ==================================================

    def _get_column_locator_by_index(self, index: int) -> Locator:
        """
        Returns the Locator for a column by its index (0-based).
        """
        self.log.info("Getting Column locator by its index.")
        return self.columns.nth(index)

    def _get_column_status(self, column: Locator) -> str:
        """
        Returns the status (name) of a given column, e.g. 'To Do'.
        """
        self.log.info("Getting Column Status (TO DO, In Progress etc...).")
        header = column.locator(LIST_NAME_SELECTOR)
        return header.inner_text().strip()

    def _get_cards_in_column(self, column: Locator) -> Locator:
        """
        Returns a Locator for all cards in the given column.
        """
        self.log.info("Get All Cards in A Column.")
        return column.locator(LIST_CARD_SELECTOR)

    def _get_card_title(self, card: Locator) -> str:
        """
        Returns the title of a given card on the board.
        """
        self.log.info("Getting Card Title.")
        return card.locator(CARD_TITLE_SELECTOR).inner_text().strip()

    def _get_card_labels_on_board(self, card: Locator) -> list[str]:
        """
        Returns the labels shown on the board (compact labels) for a given card.
        """
        self.log.info("Getting Card Label on the Board.")
        return [
            t.strip()
            for t in card.locator(COMPACT_LABEL_SELECTOR).all_inner_texts()
        ]

    def _open_card_and_get_details(self, card: Locator) -> tuple[str, str, list[str]]:
        """
        Clicks the card, waits for modal, reads title + description + labels, closes modal.
        Returns (title, description, labels).
        """
        self.log.info("Opening card modal...")
        card.click()
        self.card_modal_title.wait_for(state="visible", timeout=10_000)

        modal_title = self.get_opened_card_title()
        self.log.info(f"Card modal opened: Title='{modal_title}'")
        modal_description = self.get_opened_card_description()
        self.log.info("Description extracted.")
        modal_labels = self.get_opened_card_labels()
        self.log.info(f"Labels extracted: {modal_labels}")

        self.close_card_modal()
        self.log.info("Modal closed.")
        return modal_title, modal_description, modal_labels

    def _iter_cards_with_status(self):
        """
        Helper that yields (card_locator, status_string) for every card on the board.
        """
        self.log.info("Getting status for every card on the board.")
        column_count = self.columns.count()

        for i in range(column_count):
            column = self._get_column_locator_by_index(i)
            status = self._get_column_status(column)
            cards_in_column = self._get_cards_in_column(column)
            card_count = cards_in_column.count()

            for j in range(card_count):
                card = cards_in_column.nth(j)
                yield card, status

    # ==================================================
    # Card modal methods
    # ==================================================

    def open_card_by_title(self, title: str) -> None:
        """
        Clicks on a card with the given title on the board to open its modal.
        """
        card = self.cards.filter(has_text=title).first
        self.log.info("Opening a Card Modal by Title.")
        card.click()
        self.card_modal.wait_for(state="visible", timeout=5_000)

    def get_opened_card_title(self) -> str:
        """
        Return the title of the currently opened card modal.
        """
        self.log.info("Get Card Modal Title.")
        return self.card_modal_title.input_value().strip()

    def get_opened_card_description(self) -> str:
        """
        Returns the card description text.
        - If a description exists: read from description-content-area.
        - If the description is empty and only the 'description-button' is shown:
        return an empty string.
        """

        # Case 1: description already exists
        if self.card_modal_description_content.count() > 0:
            elem = self.card_modal_description_content.first
            elem.wait_for(state="visible", timeout=5_000)
            self.log.info("Get Card Modal Description.")
            text = elem.inner_text().strip()
            return " ".join(text.split())

        # Case 2: no description yet (only the "Add a more detailed description..." button)
        if self.card_modal_description_button.count() > 0:
            btn = self.card_modal_description_button.first
            self.log.info("Description is empty.")
            btn.wait_for(state="visible", timeout=5_000)
            # Business-wise: description is logically empty here
            return ""

        # Fallback: nothing found
        self.log.warning("No description area or button found in card modal.")
        return ""

    def get_opened_card_labels(self) -> list[str]:
        """
        Return the labels of the currently opened card modal.
        """
        self.log.info("Get Card Modal Labels.")
        label_count = self.card_modal_labels.count()
        labels: list[str] = []
        for i in range(label_count):
            label = self.card_modal_labels.nth(i)
            labels.append(label.inner_text().strip())
        return labels

    def close_card_modal(self) -> None:
        """
        Closes the currently opened card modal.
        """
        self.log.info("Closing Card Modal.")
        self.card_modal_close_button.click()
        self.card_modal.wait_for(state="hidden", timeout=5_000)

    # ==================================================
    # Scenario-specific methods
    # ==================================================

    def get_card_status_on_board(self, title: str) -> str:
        """
        Finds the status (column name) for the card with the given title.
        """
        self.log.info(f"Searching for card '{title}' on the board to get its status...")
        for card, status in self._iter_cards_with_status():
            if self._get_card_title(card) == title:
                self.log.info(f"Card '{title}' found in column '{status}'")
                return status
        raise ValueError(f"Card with title '{title}' not found on board.")

    def get_card_info(self, title: str) -> CardInfo:
        """
        Scenario 2 helper:
        - find card's status on the board
        - open card
        - read title, description, labels from modal
        - close modal
        - return CardInfo
        """
        self.log.info(f"Gathering full info for card '{title}'...")
        status = self.get_card_status_on_board(title)

        # find the card on the board and reuse the same open+read helper
        card = self.cards.filter(has_text=title).first
        modal_title, modal_description, modal_labels = self._open_card_and_get_details(card)

        return CardInfo(
            title=modal_title,
            description=modal_description,
            labels=modal_labels,
            status=status,
        )

    def get_urgent_cards_info(self) -> list[CardInfo]:
        """
        Scenario 1 helper:
        - iterate all columns
        - for each card, check if it has an 'Urgent' label on the board
        - for each urgent card, open modal, read description + labels, close modal
        - return list of CardInfo for all urgent cards
        """
        self.log.info("Collecting all 'Urgent' cards...")
        urgent_cards: list[CardInfo] = []

        for card, status in self._iter_cards_with_status():
            labels_on_board = self._get_card_labels_on_board(card)

            if "Urgent" not in labels_on_board:
                continue  # Not an urgent card

            modal_title, modal_description, modal_labels = self._open_card_and_get_details(card)

            urgent_cards.append(
                CardInfo(
                    title=modal_title,
                    description=modal_description,
                    labels=modal_labels,
                    status=status,
                )
            )

        return urgent_cards
