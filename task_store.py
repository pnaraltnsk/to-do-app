"""Task storage module for the To-Do List App."""

import json, os

FILE = "tasks.json"



def _load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def _next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def get_all_tasks():
    """Return a list of all task dicts."""
    return _load()

def add_task(title, deadline=""):
    """Create a new task. Returns the new task dict."""
    if not title.strip():
        raise ValueError("Title cannot be empty")
    tasks = _load()
    task = {
        "id": _next_id(tasks), 
        "title": title.strip(), 
        "done": False,
        "deadline": deadline.strip()
        }
    tasks.append(task)
    _save(tasks)
    return task

def toggle_done(task_id):
    """Flag a task done. Returns the updated task."""
    tasks = _load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            _save(tasks)
            return t
    raise ValueError(f"Task {task_id} not found")

def rename_task(task_id, new_title):
    """Rename a task. Returns the updated task."""
    if not new_title.strip():
        raise ValueError("Title cannot be empty")
    tasks = _load()
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = new_title.strip()
            _save(tasks)
            return t
    raise ValueError(f"Task {task_id} not found")

def update_deadline(task_id, deadline):
    """Update deadline of a task. Returns the updated task."""
    tasks = _load()
    for t in tasks:
        if t["id"] == task_id:
            t["deadline"] = deadline.strip()
            _save(tasks)
            return t
    raise ValueError(f"Task {task_id} not found")

def remove_task(task_id):
    """Delete a task by ID."""
    tasks = _load()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        raise ValueError(f"Task {task_id} not found")
    _save(new_tasks)


if __name__ == "__main__":
    if os.path.exists(FILE):
        os.remove(FILE)

    add_task("Buy milk")
    add_task("Read a book")
    add_task("Walk the dog")
    toggle_done(1)
    rename_task(2, "Read Clean Code")
    remove_task(3)

    for task in get_all_tasks():
        status = "✅" if task["done"] else "⬜"
        print(f"[{task['id']}] {status} {task['title']}")
