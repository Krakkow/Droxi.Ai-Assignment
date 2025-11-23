"""
Central place for configuration and constants
"""
import os
from dotenv import load_dotenv

# load variables from .env file into environment
load_dotenv()

#Trello API details
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY", "")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN", "")

TRELLO_BOARD_ID = "2GzdgPlw"

#Gmail API details
GMAIL_TOKEN_FILE = "./token.json"
GMAIL_CREDENTIALS_FILE = "./credentials.json"

