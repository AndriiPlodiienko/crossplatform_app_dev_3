import tkinter as tk
from tkinter import messagebox


class ModelApp:
    def __init__(self):
        self.tasks = []

    def add_task(self, title):
        title = title.strip()
        if not title:
            return False
        self.tasks.append({"title": title, "done": False})
        return True

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            return True
        return False

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["done"] = not self.tasks[index]["done"]
            return True
        return False

    def get_tasks(self):
        return list(self.tasks)

    def get_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        return total, done


class ViewApp(tk.Frame):
    def __init__(self, master, on_add, on_delete, on_toggle):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_input(on_add)
        self._build_list(on_toggle)
        self._build_controls(on_delete, on_toggle)
        self._build_stats()

    def _build_input(self, on_add):
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, pady=(0, 5))

        self.entry = tk.Entry(frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", lambda e: on_add())

        tk.Button(frame, text="Add", command=on_add, width=8).pack(side=tk.LEFT)

    def _build_list(self, on_toggle):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            frame,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            height=10,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-1>", lambda e: on_toggle())

        scrollbar.config(command=self.listbox.yview)

    def _build_controls(self, on_delete, on_toggle):
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, pady=(5, 0))

        tk.Button(frame, text="Mark Done / Undo", command=on_toggle, width=16).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(frame, text="Delete", command=on_delete, width=8).pack(side=tk.LEFT)

    def _build_stats(self):
        self.stats_label = tk.Label(self, text="", font=("Arial", 10), anchor="w")
        self.stats_label.pack(fill=tk.X, pady=(5, 0))

    def get_entry_text(self):
        return self.entry.get()

    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def get_selected_index(self):
        sel = self.listbox.curselection()
        return sel[0] if sel else None

    def update_tasks(self, tasks):
        self.listbox.delete(0, tk.END)
        for i, task in enumerate(tasks):
            prefix = "✓ " if task["done"] else "○ "
            self.listbox.insert(tk.END, prefix + task["title"])
            if task["done"]:
                self.listbox.itemconfig(i, fg="gray")

    def update_stats(self, total, done):
        self.stats_label.config(text=f"Tasks: {total}  |  Done: {done}  |  Remaining: {total - done}")

    def show_error(self, message):
        messagebox.showerror("Error", message)


class ControllerApp:
    def __init__(self, root):
        self.model = ModelApp()
        self.view = ViewApp(
            root,
            on_add=self.on_add_click,
            on_delete=self.on_delete_click,
            on_toggle=self.on_toggle_click,
        )
        self.update_view()

    def on_add_click(self):
        text = self.view.get_entry_text()
        if self.model.add_task(text):
            self.view.clear_entry()
            self.update_view()
        else:
            self.view.show_error("Please enter a task title.")

    def on_delete_click(self):
        index = self.view.get_selected_index()
        if index is None:
            self.view.show_error("Please select a task to delete.")
            return
        self.model.delete_task(index)
        self.update_view()

    def on_toggle_click(self):
        index = self.view.get_selected_index()
        if index is None:
            self.view.show_error("Please select a task to mark.")
            return
        self.model.toggle_task(index)
        self.update_view()

    def update_view(self):
        self.view.update_tasks(self.model.get_tasks())
        self.view.update_stats(*self.model.get_stats())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry("450x380")
    app = ControllerApp(root)
    root.mainloop()
