from playwright.sync_api import sync_playwright

# We use the same board url as in TrelloClient
TRELLO_BOARD_URL = "https://trello.com/b/2GzdgPlw/droxi"

def main():
    with sync_playwright() as p:
        #headless= False = visible browser for manual login
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(TRELLO_BOARD_URL)

        print(
            "\n=== Trello auth setup ===\n"
            "1. In the opened browser, click 'Log in' / 'Log in with Google'.\n"
            "2. Log in with the provided Droxi Google account.\n"
            "3. Complete any 2FA / SMS steps.\n"
            "4. Make sure you see the 'droxi' board.\n"
            "5. Then come back here; after the timeout the session will be saved.\n"
        )

        # You have 3 minutes to log in and land on the board.
        page.wait_for_timeout(3 * 60 * 1000)

        # Save the authenticated state to a file
        context.storage_state(path="trello_auth_state.json")
        print("Trello authentication state saved to 'trello_auth_state.json'.")

        browser.close()

if __name__ == "__main__":
    main()