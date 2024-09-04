import tkinter as tk
from tkinter import ttk
import sv_ttk
from ui.main_window import MainWindow


def main():
    root = tk.Tk()
    root.title("HuePy - Color Space Explorer")

    app = MainWindow(root)
    app.pack(fill=tk.BOTH, expand=True)

    root.minsize(600, 400)
    sv_ttk.set_theme("dark")
    root.mainloop()


if __name__ == "__main__":
    main()
