import tkinter as tk
from tkinter import ttk

import sv_ttk


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Color space selector
        self.color_space_label = tk.StringVar()
        self.color_space_label.set("RGB")
        color_spaces = ["RGB", "HSV", "HSL"]

        selector_frame = ttk.Frame(self)
        selector_frame.pack(pady=10)

        ttk.Label(selector_frame, text="Select Color Space:").pack(side=tk.LEFT)
        color_space_menu = ttk.Combobox(
            selector_frame, textvariable=self.color_space_label, values=color_spaces
        )
        color_space_menu.pack(side=tk.LEFT)
        color_space_menu.bind("<<ComboboxSelected>>", self.on_color_space_change)

    def on_color_space_change(self, event):
        new_color_space = self.color_space_label.get()
