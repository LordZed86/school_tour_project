# gui/shop_window.py

import tkinter as tk

class ShopWindow(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master)
        self.title("Shop")
        self.game_state = game_state
        tk.Label(self, text="Shop Window").pack(pady=10)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)