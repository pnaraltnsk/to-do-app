"""
widgets, and layout of To-Do GUI Application
"""

from pathlib import Path
import ctypes
import sys
from tkcalendar import Calendar

from tkinter import (
    Entry, Frame, Label, PhotoImage,
    Scrollbar, VERTICAL, StringVar, ttk,
)

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")
IMAGE_REFS = []



def relative_to_assets(path: str) -> Path:
    """Get the path to an asset from the assets folder."""
    return ASSETS_PATH / Path(path)


def load_photo_image(path: str, size=None):
    """Loading an image as a PhotoImage, with optional resizing."""
    try:
        image = PhotoImage(file=path)
    except Exception:
        if Image is None or ImageTk is None:
            raise
        image = ImageTk.PhotoImage(Image.open(path))
    IMAGE_REFS.append(image)
    return image


def enable_dpi_awareness():
    """DPI awareness to prevent blurry UI"""
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def center_window(window, width, height):
    """Center the window on the screen."""
    window.update_idletasks()
    x = int((window.winfo_screenwidth() - width) / 2)
    y = int((window.winfo_screenheight() - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


class ImageButton(Label):
    """ Button with an image."""
    def __init__(self, master=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self._command = command
        self.configure(cursor="hand2")
        self.bind("<Button-1>", self._invoke)

    def _invoke(self, event):
        if self._command is not None:
            self._command()

    def configure(self, cnf=None, **kwargs):
        if cnf and "command" in cnf:
            cnf = dict(cnf)
            self._command = cnf.pop("command")
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        return super().configure(cnf, **kwargs)

    config = configure


def bordered_image_button(parent, image, command, bg="#FFFFFF"):
    """Button with an image and a border."""
    outer = Frame(
        parent,
        bg="black",
        bd=0,
    )

    inner_frame = Frame(
        outer,
        bg="#F4F4F4",
        bd=0,
    )
    inner_frame.pack(padx=1, pady=1)

    inner = ImageButton(
        inner_frame,
        image=image,
        command=command,
        borderwidth=0,
        highlightthickness=0,
        bg="#F4F4F4",
        relief="flat",
    )
    inner.image = image
    inner.pack(padx=0.5, pady=0.5)

    return outer, inner

def add_placeholder(entry, placeholder, color_hint="#AAAAAA", color_real="#000716"):
    """Add placeholder text to an Entry widget."""
    entry.placeholder_text = placeholder
    entry.placeholder_on = True
    entry.placeholder_color = color_hint
    entry.real_color = color_real

    def show_placeholder():
        entry.delete(0, "end")
        entry.insert(0, entry.placeholder_text)
        entry.config(fg=entry.placeholder_color)
        entry.placeholder_on = True

    def hide_placeholder():
        if entry.placeholder_on:
            entry.delete(0, "end")
            entry.config(fg=entry.real_color)
            entry.placeholder_on = False

    def on_focus_in(e):
        hide_placeholder()

    def on_focus_out(e):
        if not entry.get().strip():
            show_placeholder()

    show_placeholder()
    entry.bind("<FocusIn>", on_focus_in, add="+")
    entry.bind("<FocusOut>", on_focus_out, add="+")


def build_ui(window, handlers: dict) -> dict:
    """Construction the UI and return references to important widgets."""
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(2, weight=1)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Todo.Treeview",
        background="#FFFFFF",
        foreground="#000000",
        fieldbackground="#FFFFFF",
        font=("Nunito SemiBold", 12),
        rowheight=30,
        borderwidth=0,
    )
    style.configure(
        "Todo.Treeview.Heading",
        font=("Nunito SemiBold", 11, "bold"),
        background="#CFE3FF",
        foreground="#333333",
        relief="flat",
    )
    style.map(
        "Todo.Treeview",
        background=[("selected", "#CFE3FF")],
        foreground=[("selected", "#000000")],
    )

    main_frame = Frame(window, bg="#CFE3FF", padx=20, pady=18)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)

    header_image = load_photo_image(relative_to_assets("image_1.png"))
    header_label = Label(main_frame, image=header_image, bg="#CFE3FF")
    header_label.image = header_image
    header_label.grid(row=0, column=0, pady=(0, 16))

    form_frame = Frame(main_frame, bg="#CFE3FF")
    form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
    form_frame.grid_columnconfigure(1, weight=1)
    form_frame.grid_columnconfigure(3, weight=0)

    Label(
        form_frame,
        text="Task:",
        bg="#CFE3FF",
        fg="#333333",
        font=("Nunito SemiBold", 11),
    ).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6))

    entry_var = StringVar()
    entry_1 = Entry(
        form_frame,
        textvariable=entry_var,
        bd=1,
        relief="solid",
        bg="#FFFFFF",
        fg="#000716",
        insertbackground="#000716",
        highlightthickness=0,
        font=("Nunito SemiBold", 12),
    )
    entry_1.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 12), ipady=8)
    add_placeholder(entry_1, "Enter task title...")

    Label(
        form_frame,
        text="Deadline:",
        bg="#CFE3FF",
        fg="#333333",
        font=("Nunito SemiBold", 11),
    ).grid(row=0, column=2, sticky="w", padx=(0, 8), pady=(0, 6))

    deadline_var = StringVar()
    deadline_display = Entry(
        form_frame,
        textvariable=deadline_var,
        bd=1,
        relief="solid",
        bg="#FFFFFF",
        fg="#000716",
        state="readonly",
        readonlybackground="#FFFFFF",
        highlightthickness=0,
        font=("Nunito SemiBold", 11),
        width=14,
    )
    deadline_display.grid(row=1, column=2, sticky="ew", padx=(0, 12), ipady=8)

    def add_readonly_placeholder(entry, placeholder):
        entry.config(state="normal")
        entry.delete(0, "end")
        entry.insert(0, placeholder)
        entry.config(fg="#AAAAAA", state="readonly")

    add_readonly_placeholder(deadline_display, "DD/MM/YYYY")

    button_image_3 = load_photo_image(relative_to_assets("button_add.png"))
    button_3 = ImageButton(
        form_frame,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        bg="#CFE3FF",
        command=handlers["add"],
        relief="flat",
    )
    button_3.image = button_image_3
    button_3.grid(row=1, column=3, sticky="e")

    cal_frame = Frame(
        window,
        bg="#FFFFFF",
        relief="flat",
        highlightbackground="#B0CCF0",
        highlightthickness=1,
    )

    cal = Calendar(
        cal_frame,
        selectmode="day",
        date_pattern="dd/mm/yyyy",
        background="#89B4FF",
        foreground="white",
        headersbackground="#CFE3FF",
        headersforeground="#333333",
        selectbackground="#89B4FF",
        font=("Nunito SemiBold", 10),
        borderwidth=0,
    )
    cal.pack()

    def on_date_selected(event=None):
        deadline_var.set(cal.get_date())
        deadline_display.config(fg="#000716")
        cal_frame.place_forget()

    cal.bind("<<CalendarSelected>>", on_date_selected)

    def toggle_calendar():
        if cal_frame.winfo_ismapped():
            cal_frame.place_forget()
        else:
            deadline_display.update_idletasks()
            x = deadline_display.winfo_rootx() - window.winfo_rootx() - 50
            y = deadline_display.winfo_rooty() - window.winfo_rooty() + \
                    deadline_display.winfo_height() + 4
            cal_frame.place(in_=window, x=x, y=y)
            cal_frame.lift()

    deadline_display.bind("<Button-1>", lambda e: toggle_calendar())

    tabs_frame = Frame(main_frame, bg="#CFE3FF")
    tabs_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
    tabs_frame.grid_columnconfigure(0, weight=1)
    tabs_frame.grid_columnconfigure(1, weight=1)

    btn_active = Label(
        tabs_frame,
        text="Active",
        bg="#89B4FF",
        fg="#000000",
        font=("Nunito SemiBold", 12),
        cursor="hand2",
        padx=20,
        pady=8,
        relief="solid",
        bd=1,
    )
    btn_active.grid(row=0, column=0, sticky="ew", padx=(80, 6))
    btn_active.bind("<Button-1>", lambda e: handlers["show_active"]())

    btn_completed = Label(
        tabs_frame,
        text="Complete",
        bg="#AFC9EE",
        fg="#000000",
        font=("Nunito SemiBold", 12),
        cursor="hand2",
        padx=20,
        pady=8,
        relief="solid",
        bd=1,
    )
    btn_completed.grid(row=0, column=1, sticky="ew", padx=(6, 80))
    btn_completed.bind("<Button-1>", lambda e: handlers["show_completed"]())

    list_card = Frame(main_frame, bg="#FFFFFF", bd=1, relief="solid")
    list_card.grid(row=3, column=0, sticky="nsew")
    list_card.grid_columnconfigure(0, weight=1)
    list_card.grid_rowconfigure(0, weight=1)

    tree_frame = Frame(list_card, bg="#FFFFFF")
    tree_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    tree_frame.grid_columnconfigure(0, weight=1)
    tree_frame.grid_rowconfigure(0, weight=1)

    scrollbar = Scrollbar(tree_frame, orient=VERTICAL)
    scrollbar.grid(row=0, column=1, sticky="ns")

    tree = ttk.Treeview(
        tree_frame,
        style="Todo.Treeview",
        columns=("task", "deadline", "id"),
        show="headings",
        yscrollcommand=scrollbar.set,
        selectmode="browse",
    )
    tree.heading("task", text="Task", command=lambda: handlers["sort_by"](tree, "task", False))
    tree.heading("deadline", text="Deadline", command=lambda: handlers["sort_by"](tree, "deadline", False))
    tree.heading("id", text="ID")
    tree.column("task", anchor="w", width=280)
    tree.column("deadline", anchor="center", width=130)
    tree.column("id", anchor="center", width=0, stretch=False)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.config(command=tree.yview)

    tree.tag_configure("done", foreground="#4CAF50")
    tree.tag_configure("active", foreground="#000000")
    tree["displaycolumns"] = ("task", "deadline")
    tree.bind("<<TreeviewSelect>>", handlers["on_select"])

    footer_frame = Frame(main_frame, bg="#CFE3FF")
    footer_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
    footer_frame.grid_columnconfigure(0, weight=1)

    count_label = Label(
        footer_frame,
        text="",
        bg="#CFE3FF",
        fg="#555555",
        font=("Nunito SemiBold", 10),
    )
    count_label.grid(row=0, column=0, sticky="w")

    actions_frame = Frame(footer_frame, bg="#CFE3FF")
    actions_frame.grid(row=0, column=1, sticky="e")

    button_image_4 = load_photo_image(relative_to_assets("button_done.png"))
    button_4 = ImageButton(
        actions_frame,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        bg="#CFE3FF",
        command=handlers["mark_complete"],
        relief="flat",
    )
    button_4.image = button_image_4
    button_4.grid(row=0, column=0, padx=(0, 8))

    button_image_2 = load_photo_image(relative_to_assets("button_update.png"))
    button_2 = ImageButton(
        actions_frame,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        bg="#CFE3FF",
        command=handlers["update"],
        relief="flat",
    )
    button_2.image = button_image_2
    button_2.grid(row=0, column=1, padx=(0, 8))

    button_image_1 = load_photo_image(relative_to_assets("button_delete.png"))
    button_1 = ImageButton(
        actions_frame,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        bg="#CFE3FF",
        command=handlers["delete"],
        relief="flat",
    )
    button_1.image = button_image_1
    button_1.grid(row=0, column=2)

    return {
        "tree": tree,
        "entry_var": entry_var,
        "entry_1": entry_1,
        "deadline_var": deadline_var,
        "deadline_display": deadline_display,
        "btn_active": btn_active,
        "btn_completed": btn_completed,
        "button_2": button_2,
        "button_4": button_4,
        "count_label": count_label,
    }
