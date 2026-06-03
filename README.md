# To-Do List App

A lightweight desktop to-do list application built with Python and Tkinter. Tasks are persisted locally in a JSON file, so your list survives between sessions.

---

## Features

- **Add tasks** with an optional deadline (DD/MM/YYYY format)
- **Edit tasks** — update the title or deadline of any existing task
- **Delete tasks** — remove tasks individually
- **Mark complete** — toggle tasks between active and done
- **Active / Completed views** — switch between in-progress and finished tasks
- **Sortable columns** — click column headers to sort by task title or deadline
- **Task count** — live display of how many tasks are in the current view
- **Persistent storage** — tasks are saved automatically to `tasks.json`
- **DPI-aware** — the window is properly scaled on high-DPI displays

---

## Project Structure

```
to-do-app/
├── main.py          # Application entry point; wires UI events to business logic
├── task_store.py    # Data layer — reads/writes tasks.json (add, delete, rename, toggle, deadline)
├── ui.py            # Tkinter UI construction and layout helpers
├── assets/          # Icons and other static assets (e.g. check-list.ico)
└── tasks.json       # Auto-generated at runtime; stores all task data
```

---

## Requirements

- Python 3.8 or higher
- Tkinter (bundled with most standard Python installations)

No third-party packages are required.

---

## Installation & Running

1. **Clone the repository**

   ```bash
   git clone https://github.com/pnaraltnsk/to-do-app.git
   cd to-do-app
   ```

2. **Run the app**

   ```bash
   python main.py
   ```

   The window opens at 580 × 700 px and centres itself on screen. A `tasks.json` file will be created in the same directory on first use.

---

## Usage

| Action | How |
|---|---|
| Add a task | Type a title (max 40 characters) in the text field, optionally set a deadline, then click **Add** |
| Edit a task | Click the task in the list — its details populate the input fields — then click **Update** |
| Delete a task | Select a task and click **Delete** |
| Complete a task | Select a task and click **Mark Complete** |
| View completed tasks | Click the **Completed** tab |
| Return to active tasks | Click the **Active** tab |
| Sort the list | Click the **Task** or **Deadline** column header |

---

## Data Storage

Tasks are stored in `tasks.json` in the project root. Each task is a JSON object with the following shape:

```json
{
  "id": 1,
  "title": "Buy milk",
  "done": false,
  "deadline": "31/12/2025"
}
```

The file is read and written on every operation. No database setup is needed.

---

## Running the Storage Module Standalone

`task_store.py` includes a self-contained demo you can run directly to verify the data layer:

```bash
python task_store.py
```

This creates a temporary `tasks.json`, adds sample tasks, renames and toggles them, then prints the results.

---

## License

This project does not currently include a license file. All rights are reserved by the author unless stated otherwise.
