from playwright.sync_api import Page, Locator
from ui.common.logger import get_logger

class BasePage:
    def __init__(self, page: Page, base_url: str | None = None) -> None:
        self.page = page
        self.base_url = (base_url or "").rstrip("/") if base_url else ""
        self.log = get_logger(self.__class__.__name__)

    def open(self, path: str = "") -> None:
        """
        Opens a page using the base_url + optional path.
        if base_url is empty, we assume 'path' is a full URL.
        """
        if self.base_url:
            if path:
                url = f"{self.base_url}/{path.lstrip('/')}"
            else:
                url = self.base_url
        else:
            url = path
            
        self.page.goto(url)


    def get_element(self, selector: str) -> Locator:
        """
        Returns a Locator for the given selector.
        """
        return self.page.locator(selector)
    
    def click_element(self, selector: str) -> None:
        """
        Clicks on the element specified by the selector.
        """
        self.get_element(selector).click()

    def fill_element(self, selector: str, value: str) -> None:
        """
        Fills the element specified by the selector with the given value.
        """
        self.get_element(selector).fill(value)
    
    def get_element_text(self, selector: str) -> str:
        """
        Returns the text content of the element specified by the selector.
        """
        return self.get_element(selector).inner_text()

    def get_element_texts(self, selector: str) -> list[str]:
        """
        Returns a list of texts from all elements matching the selector.
        """
        return self.get_element(selector).all_inner_texts()
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Returns True if the element specified by the selector is visible.
        """
        return self.get_element(selector).is_visible()
    
    def wait_for_element(self, selector: str, timeout: int = 5000) -> None:
        """
        Waits for the element specified by the selector to be visible.
        """
        self.get_element(selector).wait_for(state="visible", timeout=timeout)

    def wait_for_url_contains(self, fragment: str) -> None:
        """
        Waits until the current URL contains the specified fragment.
        """
        self.page.wait_for_url(f"**{fragment}**")