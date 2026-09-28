import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk


class TaskStore:
    def __init__(self, path):
        self.path = Path(path)
        self.tasks = self._load()

    def _load(self):
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        if not isinstance(tasks, list):
            raise ValueError("Task data must be a list.")
        return tasks

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=2)

    def add(self, title):
        title = title.strip()
        if not title:
            return False
        self.tasks.append({"title": title, "done": False})
        self._save()
        return True

    def toggle(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self._save()

    def delete(self, index):
        del self.tasks[index]
        self._save()


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My To-Do List")
        self.root.geometry("480x560")
        self.root.minsize(360, 420)
        self.store = TaskStore(Path(__file__).with_name("tasks.json"))

        style = ttk.Style()
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Hint.TLabel", foreground="#5b6470")
        style.configure("Action.TButton", padding=(10, 7))

        content = ttk.Frame(root, padding=24)
        content.pack(fill="both", expand=True)
        ttk.Label(content, text="My tasks", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            content, text="A little progress, one task at a time.", style="Hint.TLabel"
        ).pack(anchor="w", pady=(3, 18))

        add_row = ttk.Frame(content)
        add_row.pack(fill="x", pady=(0, 16))
        self.task_input = ttk.Entry(add_row)
        self.task_input.pack(side="left", fill="x", expand=True, ipady=6)
        self.task_input.bind("<Return>", lambda _event: self.add_task())
        ttk.Button(add_row, text="Add task", command=self.add_task).pack(
            side="left", padx=(8, 0)
        )

        list_frame = ttk.Frame(content)
        list_frame.pack(fill="both", expand=True)
        self.task_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            activestyle="none",
            selectmode="browse",
            borderwidth=1,
            relief="solid",
            highlightthickness=0,
            selectbackground="#dce8e2",
            selectforeground="#17211c",
        )
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_list.yview)
        self.task_list.configure(yscrollcommand=scrollbar.set)
        self.task_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.task_list.bind("<Double-Button-1>", lambda _event: self.toggle_task())

        actions = ttk.Frame(content)
        actions.pack(fill="x", pady=(14, 0))
        ttk.Button(
            actions, text="Mark complete / undo", style="Action.TButton", command=self.toggle_task
        ).pack(side="left")
        ttk.Button(
            actions, text="Delete", style="Action.TButton", command=self.delete_task
        ).pack(side="right")

        self.status = ttk.Label(content, style="Hint.TLabel")
        self.status.pack(anchor="w", pady=(12, 0))
        self.refresh_tasks()
        self.task_input.focus_set()

    def refresh_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.store.tasks:
            marker = "[x]" if task["done"] else "[ ]"
            title = f"{marker}  {task['title']}"
            self.task_list.insert(tk.END, title)
            if task["done"]:
                self.task_list.itemconfigure(tk.END, foreground="#78817b")
        remaining = sum(not task["done"] for task in self.store.tasks)
        self.status.configure(text=f"{remaining} left | {len(self.store.tasks)} total")

    def selected_index(self):
        selection = self.task_list.curselection()
        return selection[0] if selection else None

    def add_task(self):
        if self.store.add(self.task_input.get()):
            self.task_input.delete(0, tk.END)
            self.refresh_tasks()
        else:
            self.task_input.focus_set()

    def toggle_task(self):
        index = self.selected_index()
        if index is not None:
            self.store.toggle(index)
            self.refresh_tasks()
            self.task_list.selection_set(index)

    def delete_task(self):
        index = self.selected_index()
        if index is not None:
            self.store.delete(index)
            self.refresh_tasks()


def main():
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()