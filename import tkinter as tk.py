import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File path for saving tasks
file_path = "tasks.json"
tasks = {}

# Functions to handle tasks
def load_tasks():
    global tasks
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                tasks.update(json.load(file))
        except json.JSONDecodeError:
            tasks = {}

def save_tasks():
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task():
    title = simpledialog.askstring("Add Task", "Enter task title:")
    if not title:
        return
    description = simpledialog.askstring("Add Task", "Enter task description:")
    priority = simpledialog.askstring("Add Task", "Enter priority (1, 2, 3):")
    due_date = simpledialog.askstring("Add Task", "Enter due date (YYYY-MM-DD):")
    task_id = len(tasks) + 1
    tasks[task_id] = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "completed": False
    }
    save_tasks()
    refresh_tasks()
    messagebox.showinfo("Task Added", f"Task '{title}' added successfully.")

def delete_task():
    task_id = simpledialog.askinteger("Delete Task", "Enter Task ID to delete:")
    if task_id in tasks:
        del tasks[task_id]
        save_tasks()
        refresh_tasks()
        messagebox.showinfo("Task Deleted", "Task deleted successfully.")
    else:
        messagebox.showerror("Error", "Task not found.")

def complete_task():
    task_id = simpledialog.askinteger("Complete Task", "Enter Task ID to complete:")
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        save_tasks()
        refresh_tasks()
        messagebox.showinfo("Task Completed", "Task marked as completed.")
    else:
        messagebox.showerror("Error", "Task not found.")

def refresh_tasks():
    listbox.delete(0, tk.END)
    for task_id, task_info in tasks.items():
        completed = "✔" if task_info["completed"] else "✘"
        listbox.insert(tk.END, f"{task_id}. {task_info['title']} ({completed})")

# GUI Setup
load_tasks()

root = tk.Tk()
root.title("To-Do List")
root.geometry("400x550")
root.configure(bg="#eeeeee")

header = tk.Label(
    root,
    text="To-Do List",
    font=("Arial", 18, "bold"),
    bg="#007bff",
    fg="#ffffff",
    pady=10
)
header.pack(fill=tk.X)

frame = tk.Frame(root, bg="#eeeeee")
frame.pack(pady=10)

listbox = tk.Listbox(
    frame,
    width=40,
    height=15,
    bg="#ffffff",
    fg="#333333",
    selectbackground="#007bff",
    selectforeground="#ffffff",
    font=("Arial", 12),
    bd=1,
    relief="solid",
)
listbox.pack(side=tk.LEFT, padx=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

btn_frame = tk.Frame(root, bg="#eeeeee")
btn_frame.pack(pady=20)

btn_style = {
    "bg": "#007bff",
    "fg": "#ffffff",
    "font": ("Arial", 12),
    "activebackground": "#0056b3",
    "activeforeground": "#ffffff",
    "relief": "raised",
    "bd": 0,
    "width": 12,
}

# Adding buttons with improved styling
buttons = [
    ("Add Task", add_task),
    ("Delete Task", delete_task),
    ("Complete Task", complete_task),
    ("Exit", root.quit),
]

for (text, command) in buttons:
    btn = tk.Button(btn_frame, text=text, command=command, **btn_style)
    btn.pack(pady=5)

refresh_tasks()
root.mainloop()
