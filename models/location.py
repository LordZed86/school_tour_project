# models/location.py

class Location:
    """Represents a location the player can visit."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.visited = 0

    def get_desc(self):
        return self.description

    def visit(self, game_state):
        """Marks this location as visited and updates the game state."""
        self.visited += 1
        game_state.visited_locations[self.name] = True
        game_state.progress()  # This will be handled in GameState or similar