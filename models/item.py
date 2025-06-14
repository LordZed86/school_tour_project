# models/item.py

class Item:
    """Represents an item that can be stored in the player's inventory."""

    def __init__(self, name, value=0, description=""):
        self.name = name
        self.value = value
        self.description = description

    def __repr__(self):
        return f"Item(name='{self.name}', value={self.value})"

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'description': self.description,
        }

    @staticmethod
    def from_dict(data):
        return Item(
            name=data['name'],
            value=data.get('value', 0),
            description=data.get('description', "")
        )