"""
Configuring Playwright to reuse the saved Trello login state (trello_auth_state.json).
That way, tests start already logged in.
"""
import sys
from pathlib import Path
import pytest

# Ensure the project root is in sys.path for imports
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    pytest-playwright provides the 'browser_context_args'.
    We're extending it to use our saved storage state from trello_auth_state.json.
    """
    return {
        **browser_context_args,
        "storage_state": "trello_auth_state.json",
    }