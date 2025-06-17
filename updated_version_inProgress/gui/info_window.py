# gui/info_window.py

import tkinter as tk

class InfoWindow(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master)
        self.title("Information")
        self.game_state = game_state
        tk.Label(self, text="Info Window").pack(pady=10)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)