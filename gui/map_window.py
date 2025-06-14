# gui/map_window.py

import tkinter as tk

class MapWindow(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master)
        self.title("Map")
        self.game_state = game_state
        tk.Label(self, text="Map Window").pack(pady=10)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)