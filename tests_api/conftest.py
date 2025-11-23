"""
This is for shared pytest fixtures for the API tests.
Whatever fixture is defined here will be discovered by Pytest
"""

import pytest
from api.gmail_client import GmailClient
from api.trello_client import TrelloClient

@pytest.fixture(scope="session")
def gmail_client():
    """
    creating a single GmailClient instance for all tests in this session
    """
    return GmailClient()

@pytest.fixture(scope="session")
def trello_client():
    """
    creating a single TrelloClient instance for all tests in this session
    """
    return TrelloClient()