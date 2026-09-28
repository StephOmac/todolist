# My To-Do List

A small desktop to-do list app built with Python's standard-library Tkinter.

The project also includes a browser-based version in `web_app.py`. The desktop
entry point and its behavior are unchanged.

## Run

```powershell
python todo_app.py
```

Add tasks in the field and press Enter or click **Add task**. Select a task and click **Mark complete / undo** to change its status; double-clicking a task does the same. Select a task and click **Delete** to remove it.

Tasks are saved to `tasks.json` beside the app, so they remain available when you reopen it. Run the checks with:

```powershell
python -m unittest
```

## Run the web app locally

Install the web dependencies into your virtual environment, then start Flask:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe web_app.py
```

Open <http://127.0.0.1:5000>. The web and desktop versions use the same
`tasks.json` format. Set `TASKS_FILE` to choose another storage location.

## Deploy to Render

The included `render.yaml` describes a Render web service and a persistent disk
for task storage. Push this project to a Git repository, create a new Blueprint
on Render, and select that repository. The service uses Gunicorn in production.
The persistent disk requires a paid Render instance.

The web app currently has one shared list and no sign-in. Anyone who can reach
the deployed URL can view, add, complete, and delete its tasks; add authentication
before putting private tasks there.

## Deploy to Vercel

The root `app.py` exposes the Flask instance for Vercel's Python runtime, and
`vercel.json` configures its function. Import this repository as a new Vercel
project, keep the project root at the repository root, and deploy; Vercel detects
the Python dependencies from `requirements.txt`. You can also deploy with the
Vercel CLI using `vercel` from the project directory.

Set a `SECRET_KEY` environment variable in the Vercel project settings before
deploying. On Vercel, tasks are written to `/tmp/tasks.json` because the deployed
filesystem is not persistent. This is only suitable for a demo: tasks may
disappear or differ between function instances. For lasting shared tasks, connect
an external database or persistent storage service and replace the JSON storage.
The app remains a single shared list without sign-in.