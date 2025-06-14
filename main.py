# main.py

import tkinter as tk
from models.game_state import GameState
from gui.main_window import MainWindow


def main():
    game = GameState()
    root = tk.Tk()
    app = MainWindow(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()