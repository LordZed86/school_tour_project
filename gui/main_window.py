# gui/main_window.py

import tkinter as tk
from tkinter import messagebox
from models.location import Location
from models.item import Item


class MainWindow:
    def __init__(self, root, game_state):
        self.root = root
        self.game_state = game_state
        self.root.title("School Tour Game")

        self.label_location = tk.Label(root, text="", font=("Arial", 14))
        self.label_location.pack(pady=10)

        self.label_inventory = tk.Label(root, text="", font=("Arial", 12))
        self.label_inventory.pack(pady=10)

        self.button_visit = tk.Button(root, text="Visit Library", command=self.visit_library)
        self.button_visit.pack(pady=5)

        self.button_add_item = tk.Button(root, text="Get Free Map", command=self.get_map)
        self.button_add_item.pack(pady=5)

        self.button_quit = tk.Button(root, text="Quit", command=root.quit)
        self.button_quit.pack(pady=20)

        self.refresh()

    def visit_library(self):
        location = Location("Library", "A quiet place to study and read.")
        self.game_state.move_to(location)
        self.refresh()

    def get_map(self):
        map_item = Item("Map", 0, "A free campus map.")
        self.game_state.add_item(map_item)
        self.refresh()

    def refresh(self):
        loc = self.game_state.stats['cur_loc']
        location_text = f"Current Location: {loc}" if loc else "No location visited yet"
        self.label_location.config(text=location_text)

        inv_text = "Inventory: " + ", ".join([item.name for item in self.game_state.inventory])
        self.label_inventory.config(text=inv_text)