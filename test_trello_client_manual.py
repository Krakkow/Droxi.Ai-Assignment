"""
Small manual check to see that TrelloClient works.
This is NOT part of the final assignment tests – just for us.
"""

from api.trello_client import TrelloClient


def main():
    client = TrelloClient()

    # Get lists (columns)
    lists = client.get_board_lists()
    print("Board lists (columns):")
    for lst in lists:
        print(f"- {lst.get('name')} (id={lst.get('id')})")

    #Build a list_id -> list_nam
    lists_map = client.build_lists_map()

    print("\nSome cards on the board:")
    cards = client.get_board_cards()
    
    # Print only first 5 cards to keep output short
    for card in cards[:5]:
        card_title = card.get("name")
        card_list_id = card.get("idList")
        card_labels = [label.get("name") for label in card.get("labels", [])]

        # Use the map to find the column name
        column_name = lists_map.get(card_list_id)

        print(f" Title: {card_title}")
        print(f" Column: {column_name}")
        print(f" Labels: {card_labels}")
        print("")


if __name__ == "__main__":
    main()
