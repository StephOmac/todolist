# AGENTS.md

## Project overview
This project is a Python to-do list app that started as a desktop Tkinter app and was expanded into a browser-based Flask app for local use and deployment.

The project currently includes:
- a desktop app in `todo_app.py`
- a web app in `web_app.py`
- a Vercel-friendly entrypoint in `app.py`
- persistent JSON task storage via `tasks.json`
- deployment configs for Render and Vercel

## Current project state
- Python version used for development: 3.14.5
- Virtual environment: `.venv`
- Web framework: Flask
- Local web app URL: `http://127.0.0.1:5000`
- Verified test status: 7 tests passing

## Important project files
- `todo_app.py` — original desktop Tkinter app
- `web_app.py` — Flask app used for browser version
- `app.py` — Vercel entrypoint that exports the Flask app
- `tasks.json` — JSON file used to store tasks in the same format for desktop and web apps
- `templates/index.html` — browser UI
- `requirements.txt` — Python dependencies for the web app
- `render.yaml` — Render deployment config
- `vercel.json` — Vercel deployment config
- `.python-version` — Python version pin used for Vercel
- `test_todo_app.py` — tests for desktop task logic
- `test_web_app.py` — tests for browser routes and task persistence
- `README.md` — usage and deployment notes

## How to run locally

### Desktop app
```powershell
python todo_app.py
```

### Web app
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe web_app.py
```
Then open:
```text
http://127.0.0.1:5000
```

## Verified commands
These commands were successfully used during development:

```powershell
.venv\Scripts\python.exe -m unittest -v
```

```powershell
.venv\Scripts\python.exe web_app.py
```

```powershell
.venv\Scripts\python.exe -c "from pathlib import Path; from tempfile import TemporaryDirectory; from web_app import create_app; d=TemporaryDirectory(); p=Path(d.name)/'tasks.json'; c=create_app(p).test_client(); assert c.get('/').status_code == 200; assert c.post('/tasks', data={'title':'Check web'}, follow_redirects=True).status_code == 200; assert p.read_text(encoding='utf-8').find('Check web') >= 0; assert c.post('/tasks/0/toggle').status_code == 302; assert 'true' in c.get('/').get_data(as_text=True); assert c.post('/tasks/0/delete').status_code == 302; assert 'Check web' not in c.get('/').get_data(as_text=True); d.cleanup(); print('Web CRUD smoke check passed')"
```

## Storage and deployment notes

### Local behavior
The app stores tasks in `tasks.json` using a simple JSON array structure:
```json
[
  { "title": "Sample task", "done": false }
]
```
This is used by both the desktop and web versions.

### Vercel behavior
For Vercel, the app is configured to use:
- entrypoint: `app.py`
- function config: `vercel.json`
- Python version: `3.14`

Because Vercel functions run in a temporary filesystem, writes go to `/tmp/tasks.json` when deployed there. This means the app works as a demo in Vercel, but task data is not durable across cold starts or redeploys.

### Render behavior
Render is configured via `render.yaml` with a persistent disk for `tasks.json`, which is more suitable for longer-lived task data.

## Security and usage notes
- There is currently no user authentication.
- Anyone who can access the deployed URL can view and alter the shared to-do list.
- For private or production usage, add authentication and a database-backed storage layer.

## Deployment checklist
Before deploying to any public platform:
1. Set `SECRET_KEY` in environment variables.
2. Confirm the platform uses the project root as the app root.
3. Keep `requirements.txt` in sync with the app dependencies.
4. Decide whether the task storage should remain JSON, be moved to a database, or use a platform-managed volume.

## Summary
This project demonstrates a Python to-do app built in two modes:
- a desktop version for local use
- a web version for deployment

The current verified state is that the app and tests work locally, and the project is prepared for Vercel and Render deployment with the caveat that JSON file storage is not production-persistent on Vercel without external storage.
