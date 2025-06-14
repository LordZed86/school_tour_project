# gui/main_window.py

import tkinter as tk
from tkinter import messagebox
from models.location import Location
from models.item import Item
from gui.shop_window import ShopWindow
from gui.map_window import MapWindow
from gui.info_window import InfoWindow
from gui.inventory_window import InventoryWindow
from gui.save_load_window import SaveLoadWindow

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
        
        self.button_shop = tk.Button(root, text="Open Shop", command=self.open_shop)
        self.button_shop.pack(pady=5)

        self.button_map = tk.Button(root, text="Open Map", command=self.open_map)
        self.button_map.pack(pady=5)

        self.button_info = tk.Button(root, text="Game Info", command=self.open_info)
        self.button_info.pack(pady=5)

        self.button_inventory = tk.Button(root, text="Inventory", command=self.open_inventory)
        self.button_inventory.pack(pady=5)

        self.button_save_load = tk.Button(root, text="Save / Load", command=self.open_save_load)
        self.button_save_load.pack(pady=5)

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
        
    def open_shop(self):
        ShopWindow(self.root, self.game_state)

    def open_map(self):
        MapWindow(self.root, self.game_state)

    def open_info(self):
        InfoWindow(self.root, self.game_state)

    def open_inventory(self):
        InventoryWindow(self.root, self.game_state)

    def open_save_load(self):
        SaveLoadWindow(self.root, self.game_state)