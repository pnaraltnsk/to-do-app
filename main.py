"""Main application file for the To-Do List App."""
from tkinter import Tk, StringVar, END, messagebox
from ui import build_ui, enable_dpi_awareness, center_window
import task_store


def main():
    """Main function to run the application."""
    enable_dpi_awareness()

    window = Tk()
    window.title("To-Do List App")
    window.geometry("580x700")
    window.configure(bg="#CFE3FF")
    center_window(window, 580, 700)
    window.resizable(True, True)

    try:
        from ui import relative_to_assets
        window.iconbitmap(relative_to_assets("check-list.ico"))
    except Exception:
        pass

    current_view = StringVar(value="active")
    refs = {}


    def get_selected_task():
        selected = refs["tree"].selection()
        if not selected:
            return None
        task_id = refs["tree"].item(selected[0], "values")[2]
        for t in task_store.get_all_tasks():
            if t["id"] == int(task_id):
                return t
        return None

    def refresh_list():
        refs["tree"].delete(*refs["tree"].get_children())
        all_tasks = task_store.get_all_tasks()

        if current_view.get() == "active":
            tasks = [t for t in all_tasks if not t["done"]]
            for t in tasks:
                refs["tree"].insert("", END, values=(t["title"], t.get("deadline", ""),
                                                     t["id"]), tags=("active",))
            refs["button_4"].grid()
            refs["button_2"].grid()
            refs["count_label"].config(text=f"{len(tasks)} task(s)")
        else:
            tasks = [t for t in all_tasks if t["done"]]
            for t in tasks:
                refs["tree"].insert("", END, values=(f"✓  {t['title']}",  t.get("deadline", ""),
                                                     t["id"]), tags=("done",))
            refs["button_4"].grid_remove()
            refs["button_2"].grid_remove()
            refs["count_label"].config(text=f"{len(tasks)} task(s) completed")

        refs["tree"]["displaycolumns"] = ("task", "deadline")


    def show_active():
        current_view.set("active")
        refs["btn_active"].config(bg="#89B4FF")
        refs["btn_completed"].config(bg="#AFC9EE")
        refresh_list()

    def show_completed():
        current_view.set("completed")
        refs["btn_active"].config(bg="#AFC9EE")
        refs["btn_completed"].config(bg="#89B4FF")
        refresh_list()


    def add():
        title = refs["entry_var"].get().strip()
        if not title or title == "Enter task title...":
            messagebox.showwarning("Empty input", "Please type a task first.")
            return
        if len(title) > 40:
            messagebox.showwarning("Too long", "Task title cannot exceed 50 characters.")
            return
        deadline = refs["deadline_var"].get()
        if deadline == "DD/MM/YYYY":
            deadline = ""

        task_store.add_task(title, deadline)
        refs["entry_1"].delete(0, END)
        refs["entry_1"].event_generate("<FocusOut>")
        refs["deadline_var"].set("DD/MM/YYYY")
        refs["deadline_display"].config(fg="#AAAAAA")

        refs["tree"].focus_set()

        if current_view.get() != "active":
            show_active()
        else:
            refresh_list()

    def delete():
        task = get_selected_task()
        if not task:
            messagebox.showinfo("No selection", "Click a task to delete it.")
            return
        task_store.remove_task(task["id"])
        refs["tree"].selection_remove(refs["tree"].selection())
        refs["entry_1"].delete(0, END)
        refs["entry_1"].event_generate("<FocusOut>")
        refs["deadline_var"].set("DD/MM/YYYY")
        refs["deadline_display"].config(fg="#AAAAAA")

        refresh_list()

    def update():
        task = get_selected_task()
        if not task:
            messagebox.showinfo("No selection", "Click a task in the list first.")
            return
        text = refs["entry_var"].get().strip()
        if not text or text == "Enter task title...":
            messagebox.showwarning("Empty input", "The task text cannot be empty.")
            return
        if len(text) > 40:
            messagebox.showwarning("Too long", "Task title cannot exceed 50 characters.")
            return
        deadline = refs["deadline_var"].get()
        if deadline == "DD/MM/YYYY":
            deadline = ""

        task_store.rename_task(task["id"], text)
        task_store.update_deadline(task["id"], deadline)

        refs["entry_1"].delete(0, END)
        refs["entry_1"].event_generate("<FocusOut>")
        refs["deadline_var"].set("DD/MM/YYYY")
        refs["deadline_display"].config(fg="#AAAAAA")

        refs["tree"].focus_set()
        refresh_list()




    def mark_complete():
        task = get_selected_task()
        if not task:
            messagebox.showinfo("No selection", "Click a task to complete it.")
            return
        task_store.toggle_done(task["id"])
        messagebox.showinfo("Done!", f'"{task["title"]}" marked as complete!')
        refs["entry_1"].delete(0, END)
        refs["entry_1"].event_generate("<FocusOut>")
        refs["deadline_var"].set("DD/MM/YYYY")
        refs["deadline_display"].config(fg="#AAAAAA")

        refs["tree"].focus_set()
        refresh_list()

    def on_select(event):
        task = get_selected_task()
        if task:
            refs["entry_1"].delete(0, END)
            refs["entry_1"].insert(0, task["title"])
            refs["entry_1"].config(fg=refs["entry_1"].real_color)
            refs["entry_1"].placeholder_on = False

            if task.get("deadline"):
                refs["deadline_var"].set(task["deadline"])
                refs["deadline_display"].config(fg="#000716")
            else:
                refs["deadline_var"].set("DD/MM/YYYY")
                refs["deadline_display"].config(fg="#AAAAAA")

    def sort_by(tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
        tree.heading(col, command=lambda: sort_by(tree, col, not descending))



    handlers = {
        "add": add,
        "delete": delete,
        "update": update,
        "mark_complete": mark_complete,
        "show_active": show_active,
        "show_completed": show_completed,
        "on_select": on_select,
        "sort_by": sort_by,
    }

    refs.update(build_ui(window, handlers))
    refresh_list()
    window.mainloop()


if __name__ == "__main__":
    main()
