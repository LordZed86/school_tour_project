# models/game_state.py

class GameState:
    """Tracks the player's current status and progress."""

    def __init__(self):
        self.stats = {
            'money': 0,
            'cur_loc': None,
            'tours': 0,
        }
        self.visited_locations = {}
        self.inventory = []

    def progress(self):
        """Updates game progress based on visited locations."""
        self.stats['tours'] = len([v for v in self.visited_locations.values() if v])

    def move_to(self, location):
        """Updates current location."""
        self.stats['cur_loc'] = location.name
        location.visit(self)

    def add_item(self, item):
        """Adds an item to the inventory."""
        self.inventory.append(item)

    def clear_inventory(self):
        self.inventory.clear()