# gui/inventory_window.py

import tkinter as tk

class InventoryWindow(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master)
        self.title("Inventory")
        self.game_state = game_state
        tk.Label(self, text="Inventory Window").pack(pady=10)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)