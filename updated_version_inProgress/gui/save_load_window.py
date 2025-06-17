# gui/save_load_window.py

import tkinter as tk

class SaveLoadWindow(tk.Toplevel):
    def __init__(self, master, game_state):
        super().__init__(master)
        self.title("Save/Load")
        self.game_state = game_state
        tk.Label(self, text="Save/Load Window").pack(pady=10)
        tk.Button(self, text="Close", command=self.destroy).pack(pady=5)