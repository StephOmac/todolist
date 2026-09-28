import json
import os
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, url_for


def create_app(data_file=None):
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")
    app.config["TASKS_FILE"] = Path(
        data_file or os.environ.get("TASKS_FILE", Path(__file__).with_name("tasks.json"))
    )

    def load_tasks():
        path = app.config["TASKS_FILE"]
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        if not isinstance(tasks, list):
            raise ValueError("Task data must be a list.")
        return tasks

    def save_tasks(tasks):
        path = app.config["TASKS_FILE"]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)

    @app.get("/")
    def index():
        tasks = load_tasks()
        remaining = sum(not task["done"] for task in tasks)
        return render_template("index.html", tasks=tasks, remaining=remaining)

    @app.post("/tasks")
    def add_task():
        title = request.form.get("title", "").strip()
        if title:
            tasks = load_tasks()
            tasks.append({"title": title, "done": False})
            save_tasks(tasks)
        else:
            flash("Write a task before adding it.")
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_index>/toggle")
    def toggle_task(task_index):
        tasks = load_tasks()
        if task_index >= len(tasks):
            abort(404)
        tasks[task_index]["done"] = not tasks[task_index]["done"]
        save_tasks(tasks)
        return redirect(url_for("index"))

    @app.post("/tasks/<int:task_index>/delete")
    def delete_task(task_index):
        tasks = load_tasks()
        if task_index >= len(tasks):
            abort(404)
        del tasks[task_index]
        save_tasks(tasks)
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))