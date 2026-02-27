import tkinter as tk


# ===================== MODEL =====================
class ModelApp:
    def __init__(self, default_style):

        self.default_style = default_style.copy()

        self.light_theme = {
            "fg": "black",
            "bg": "white",
            "bd": 2,
            "relief": "ridge",
            "highlightbackground": "lightgrey",
            "highlightcolor": "blue",
            "highlightthickness": 2,
            "justify": "center",
            "anchor": "center",
            "width": 20,
            "height": 2
        }

        self.dark_theme = {
            "fg": "white",
            "bg": "black",
            "bd": 3,
            "relief": "groove",
            "highlightbackground": "grey",
            "highlightcolor": "cyan",
            "highlightthickness": 2,
            "justify": "center",
            "anchor": "center",
            "width": 20,
            "height": 2
        }

        self.current_style = default_style.copy()

    def set_theme(self, theme):
        if theme == "light":
            self.current_style = self.light_theme.copy()
        elif theme == "dark":
            self.current_style = self.dark_theme.copy()

    def update_param(self, par, value):
        self.current_style[par] = value

    def reset_default(self):
        self.current_style = self.default_style.copy()

    def get_style(self):
        return self.current_style


# ===================== VIEW =====================
class ViewApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.available = {
            "height": [1, 2, 3],
            "width": [10, 20, 30],
            "text": ["Hello World", "Hello\nWorld"],
            "anchor": ["n", "s", "w", "e", "center"],
            "justify": ["left", "center", "right"],
            "wraplength": [40, 80],
            "padx": [0, 10, 20, 30],
            "pady": [0, 10, 20, 30],
            "cursor": ["arrow", "hand2", "cross", "watch"],
            "fg": ["black", "navy"],
            "bg": ["white", "azure", "black"],
            "activeforeground": ["blue"],
            "activebackground": ["light blue"],
            "bd": [0, 2, 5],
            "relief": ["flat", "raised", "sunken", "ridge", "groove", "solid"],
            "highlightbackground": ["light grey", "grey"],
            "highlightcolor": ["blue", "cyan"],
            "highlightthickness": [0, 2, 5],
            "state": ["normal", "disabled"],
        }

        frame_wid = tk.LabelFrame(self, text="Widget")
        frame_wid.pack(fill="x")

        self.widget = tk.Label(frame_wid)
        self.widget.pack()

        theme_frame = tk.LabelFrame(self, text="Themes")
        theme_frame.pack(fill="x")

        self.btn_light = tk.Button(theme_frame, text="LIGHT THEME")
        self.btn_dark = tk.Button(theme_frame, text="DARK THEME")

        self.btn_light.pack(side="left", fill="x", expand=True)
        self.btn_dark.pack(side="left", fill="x", expand=True)

        frame_set = tk.LabelFrame(self, text="Settings")
        frame_set.pack(fill="x")

        self.param_buttons = {}

        for par, args in self.available.items():
            frame = tk.LabelFrame(frame_set, text=par)
            frame.pack(side="left", anchor="nw", fill="y")

            for arg in args:
                btn = tk.Button(frame, text=str(arg))
                btn.pack(fill="x")
                self.param_buttons[btn] = (par, arg)

        self.btn_default = tk.Button(self, text="DEFAULT")
        self.btn_default.pack(fill="x")

    def apply_style(self, style):
        self.widget.config(**style)

    def get_default_style(self):
        return {par: self.widget.cget(par) for par in self.widget.keys()}

    def config_root(self):
        self.master.title("LAB 03 - Variant 17")
        self.master.geometry("1000x400")


# ===================== CONTROLLER =====================
class ControllerApp:
    def __init__(self, root):
        self.view = ViewApp(root)
        self.view.pack(fill="both", expand=True)
        self.view.config_root()

        default_style = self.view.get_default_style()

        self.model = ModelApp(default_style)

        self.view.btn_light.config(command=lambda: self.apply_theme("light"))
        self.view.btn_dark.config(command=lambda: self.apply_theme("dark"))
        self.view.btn_default.config(command=self.reset_default)

        for btn, (par, arg) in self.view.param_buttons.items():
            btn.config(command=lambda p=par, a=arg: self.change_param(p, a))

    def apply_theme(self, theme):
        self.model.set_theme(theme)
        self.view.apply_style(self.model.get_style())

    def change_param(self, par, arg):
        self.model.update_param(par, arg)
        self.view.apply_style(self.model.get_style())

    def reset_default(self):
        self.model.reset_default()
        self.view.apply_style(self.model.get_style())


# ===================== MAIN =====================
if __name__ == "__main__":
    root = tk.Tk()
    app = ControllerApp(root)
    root.mainloop()
