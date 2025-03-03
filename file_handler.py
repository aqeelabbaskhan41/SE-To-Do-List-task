# file_handler.py
import os

FILE_NAME = "todo_list.txt"

def load_tasks():
    """Loads tasks from a file and returns them as a list."""
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        tasks = [line.strip() for line in file.readlines()]
    return tasks

def save_task(task):
    """Appends a new task to the file."""
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(task + "\n")

def delete_tasks(indices_to_remove):
    """Deletes tasks by index from the file."""
    tasks = load_tasks()  # Load current tasks
    new_tasks = [task for i, task in enumerate(tasks) if i not in indices_to_remove]

    # Rewrite file with remaining tasks
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for task in new_tasks:
            file.write(task + "\n")

def edit_task(index, updated_task):
    """Edits a task at a specific index in the file."""
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index] = updated_task  # Update task

    # Rewrite file with updated tasks
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")
