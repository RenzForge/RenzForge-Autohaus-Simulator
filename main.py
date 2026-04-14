from gui import AutoGUI
import tkinter as tk
from config import Config

if __name__ == "__main__":
    config = Config()
    root = tk.Tk()
    app = AutoGUI(root, config)
    root.mainloop()