"""
Simple wrapper around Trello REST API
Only includes methods needed for this project
"""

import requests

from config import TRELLO_API_KEY, TRELLO_API_TOKEN, TRELLO_BOARD_ID

class TrelloClient:
    """
    A very small client class to communicate with Trello API.
    """

    def __init__(self):
        self.base_url = "https://api.trello.com/1"

    def _auth_params(self):
        return {
            "key": TRELLO_API_KEY,
            "token": TRELLO_API_TOKEN
        }
    
    def get_board_cards(self) -> list:
        """
        Return all cards on the board with specified fields.
        """
        url = f"{self.base_url}/boards/{TRELLO_BOARD_ID}/cards"

        params = {
            **self._auth_params(),
            "fields": "name,desc,idList,labels"
        }

        response = requests.get(url, params=params)

        # Raise an error for bad responses
        response.raise_for_status()

        # Trello returns JSON -> Python dict/list conversion automatically
        return response.json()

    def get_board_lists(self) -> list:
        """
        return all lists (columns) on the board.
        Using this to map list_id -> list name (To Do / In Progress / Completed)
        """
        url = f"{self.base_url}/boards/{TRELLO_BOARD_ID}/lists"
        params = self._auth_params()

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()
    
    
    def build_lists_map(self) -> dict:
        """
        Building a simple dictionary: list_id -> list_name
        for example: "5f6d7e8c9b0a1b2c3d4e5f6g": "To Do"
        """
        lists = self.get_board_lists()
        lists_map = {}
        for lst in lists:
            list_id = lst.get("id")
            list_name = lst.get("name")
            if list_id:
                lists_map[list_id] = list_name
        return lists_map
    
    
    
    
    def get_list_name_by_id(self, list_id: str) -> str | None:
        """
        Helper method to get list name by its ID.
        """
        lists_map = self.build_lists_map()
        return lists_map.get(list_id)