import tkinter as tk
from tkinter import ttk
import sv_ttk


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Creates a toplevel window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        style = ttk.Style()
        bg_color = style.lookup("TLabel", "background")
        fg_color = style.lookup("TLabel", "foreground")

        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background=bg_color,
            foreground=fg_color,
            relief="solid",
            borderwidth=1,
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.sliders = []
        self.create_widgets()
        self.master.bind("<Configure>", self.on_window_resize)

    def create_widgets(self):
        # Color space selector
        self.color_space_var = tk.StringVar()
        self.color_space_var.set("RGB")  # Default to RGB
        color_spaces = ["RGB", "HSV", "HSL"]

        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Color space selector
        selector_frame = ttk.Frame(main_container)
        selector_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(selector_frame, text="Select Color Space:").pack(side=tk.LEFT)
        color_space_menu = ttk.Combobox(
            selector_frame, textvariable=self.color_space_var, values=color_spaces
        )
        color_space_menu.pack(side=tk.LEFT)
        color_space_menu.bind("<<ComboboxSelected>>", self.on_color_space_change)

        # Color sliders frame
        self.sliders_frame = ttk.Frame(main_container)
        self.sliders_frame.pack(expand=True, fill=tk.BOTH)

        # Color code text
        self.color_code_var = tk.StringVar()
        self.color_code_var.set("#000000")
        self.color_code_label = ttk.Label(
            main_container,
            textvariable=self.color_code_var,
            cursor="hand2",  # Change cursor to hand when hovering
        )
        self.color_code_label.pack(fill=tk.X, pady=(10, 5))
        self.color_code_label.bind("<Button-1>", self.copy_color_code)

        # Tooltip
        Tooltip(self.color_code_label, "Click to copy color code")

        # Color preview
        self.color_preview_frame = ttk.Frame(main_container)
        self.color_preview_frame.pack(fill=tk.X, pady=(10, 0))
        self.color_preview = tk.Canvas(main_container, height=200, bg="white")
        self.color_preview.pack(fill=tk.X, pady=(10, 0))

        # Inital setup
        self.create_sliders("RGB")

    def create_sliders(self, color_space):
        # Clear existing sliders
        for widget in self.sliders_frame.winfo_children():
            widget.destroy()
        self.sliders.clear()

        # Call appropriate function to create sliders
        if color_space == "RGB":
            self.create_rgb_sliders()
        # Add more elif blocks for other color spaces

    def create_rgb_sliders(self):
        self.r_val = tk.IntVar()
        self.g_val = tk.IntVar()
        self.b_val = tk.IntVar()

        sliders = [
            ("R", self.r_val, 0, 255),
            ("G", self.g_val, 0, 255),
            ("B", self.b_val, 0, 255),
        ]

        for label, var, min_val, max_val in sliders:
            self.create_slider(label, var, min_val, max_val)

    def create_slider(self, label, var, from_, to):
        frame = ttk.Frame(self.sliders_frame)
        frame.pack(fill=tk.X, pady=5)

        ttk.Label(frame, text=f"{label}:", width=10).pack(side=tk.LEFT)

        # Changes
        display_var = tk.StringVar()
        display_var.set(round(var.get()))

        def update_display_var(*args):
            display_var.set(round(var.get()))

        var.trace_add("write", update_display_var)

        slider = ttk.Scale(
            frame, from_=from_, to=to, variable=var, command=self.update_color
        )

        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        value_label = ttk.Label(frame, textvariable=display_var, width=5)
        value_label.pack(side=tk.LEFT)

        self.sliders.append(slider)

    def update_color(self, event):
        if self.color_space_var.get() == "RGB":
            r = self.r_val.get()
            g = self.g_val.get()
            b = self.b_val.get()
            color = f"#{r:02x}{g:02x}{b:02x}"
        else:
            color = "gray"
        self.color_preview.config(bg=color)
        self.color_code_var.set(color.upper())

    def copy_color_code(self, event):
        color_code = self.color_code_var.get()
        self.clipboard_clear()
        self.clipboard_append(color_code)
        self.update()

        original_bg = self.color_code_label.cget("background")
        self.color_code_label.config(background="lightgreen")
        self.after(200, lambda: self.color_code_label.config(background=original_bg))

    def on_color_space_change(self, event):
        new_color_space = self.color_space_var.get()

    def on_window_resize(self, event):
        # Update sliders without recreating them
        if self.sliders:
            new_width = event.width - 150
            for slider in self.sliders:
                slider.config(length=new_width)

        self.resize_color_preview()

    def resize_color_preview(self):
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        new_height = max(200, window_height // 4)

        # Update color preview size
        self.color_preview.config(height=new_height)
        self.color_preview_frame.config(height=new_height)

        self.update_color(None)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("HuePy - Color Space Explorer")

    app = MainWindow(root)
    app.pack(fill=tk.BOTH, expand=True)

    root.minsize(600, 400)
    sv_ttk.set_theme("dark")
    root.mainloop()
