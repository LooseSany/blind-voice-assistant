from datetime import datetime
import json
import os

TODO_FILE = os.path.join(os.path.dirname(__file__), "todos.json")


APP_PACKAGES = {
    "youtube": "com.google.android.youtube",
    "calculator": "com.google.android.calculator",
    "chrome": "com.android.chrome",
    "whatsapp": "com.whatsapp",
    "maps": "com.google.android.apps.maps",
}


def _load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_todos(todos):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f)


def process_command(raw):
    text = (raw or "").strip()
    cmd = text.lower()

    if cmd == "help":
        return "say||Commands: add todo <task>, show todos, clear todos, open youtube, navigate to <place>, time, date"

    if cmd.startswith("add todo "):
        task = text[9:].strip()
        if not task:
            return "say||Please provide a task"
        todos = _load_todos()
        todos.append(task)
        _save_todos(todos)
        return f"say||Added to-do: {task}"

    if cmd == "show todos":
        todos = _load_todos()
        if not todos:
            return "say||Your to-do list is empty"
        return "say||" + ", ".join(f"{i+1}. {item}" for i, item in enumerate(todos))

    if cmd == "clear todos":
        _save_todos([])
        return "say||All to-dos cleared"

    if cmd.startswith("open "):
        app_name = cmd.replace("open ", "", 1).strip()
        pkg = APP_PACKAGES.get(app_name)
        if not pkg:
            return "say||Unknown app. Try open youtube"
        return f"open_app|{pkg}|Opening {app_name}"

    if cmd.startswith("navigate to "):
        place = text[12:].strip()
        if not place:
            return "say||Please provide destination"
        return f"navigate|{place}|Starting navigation to {place}"

    if cmd == "time":
        return "say||Current time is " + datetime.now().strftime("%I:%M %p")

    if cmd == "date":
        return "say||Today is " + datetime.now().strftime("%B %d, %Y")

    return "say||Command not recognized. Say help"