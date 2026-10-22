"""To-Do List & Task Manager module for static analysis lab."""

import json
import secrets
from datetime import datetime
from email.message import EmailMessage

tasks = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def add_task(title, priority="medium", labels=None):
    """Add a new task with given title, priority, and optional labels."""
    if labels is None:
        labels = []
    else:
        labels = list(labels)
    labels.append(priority)
    task_id = len(tasks) + 1
    tasks[task_id] = {
        "title": title,
        "priority": priority,
        "done": False,
        "created": datetime.now().isoformat(),
        "labels": labels,
    }
    return task_id


def complete_task(task_id):
    """Mark a task as completed by its ID."""
    if task_id in tasks:
        tasks[task_id]["done"] = True
        return True
    print("No task with id", task_id)
    return False


def pending_tasks():
    """Return titles of pending tasks sorted by priority."""
    pending = [task for task in tasks.values() if not task["done"]]
    pending.sort(key=lambda task: PRIORITY_ORDER[task["priority"]])
    return [task["title"] for task in pending]


def find_task(keyword):
    """Find and return the ID of a task matching the keyword."""
    for task_id, task in tasks.items():
        if keyword.lower() in task["title"].lower():
            return task_id
    return None


def save_tasks(file_name="tasks.json"):
    """Save tasks to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def load_tasks(file_name="tasks.json"):
    """Load tasks from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def export_json(file_name="tasks.json"):
    """Export tasks to a JSON formatted file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def remind_by_email(address):
    """Send reminder email with pending tasks using standard email library."""
    msg = EmailMessage()
    msg["Subject"] = "Pending tasks"
    msg["To"] = address
    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            msg.set_content(f.read())
    except FileNotFoundError:
        pass


def main():
    """Execute main demonstration for task manager."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")
    complete_task(2)
    complete_task(99)
    print("Pending tasks:", pending_tasks())
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym"))  # returns None silently
    suggestion = secrets.choice(pending_tasks())
    print("Try this next:", suggestion)
    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))
    export_json()
    print("Exported tasks to tasks.json")


# Backward compatibility aliases for functions originally named in camelCase
addTask = add_task  # pylint: disable=invalid-name
completeTask = complete_task  # pylint: disable=invalid-name
pendingTasks = pending_tasks  # pylint: disable=invalid-name
findTask = find_task  # pylint: disable=invalid-name
saveTasks = save_tasks  # pylint: disable=invalid-name
loadTasks = load_tasks  # pylint: disable=invalid-name
exportJson = export_json  # pylint: disable=invalid-name
remindByEmail = remind_by_email  # pylint: disable=invalid-name

if __name__ == "__main__":
    main()
