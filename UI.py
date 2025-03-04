import tkinter as tk
from tkinter import messagebox, font
import file_handler  # Import file handling functions

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DO_TO_list app")
        self.root.attributes("-fullscreen", True)  # Full-screen mode
        self.root.configure(bg="#EAEAF5")

        # Custom Fonts
        heading_font = font.Font(family="Arial", size=16, weight="bold")
        task_font = font.Font(family="Arial", size=14)

        # Header Frame
        header_frame = tk.Frame(self.root, bg="#A268D3", height=60)
        header_frame.pack(fill="x")

        title_label = tk.Label(header_frame, text="DO_TO_list app", fg="white", bg="#A268D3", font=heading_font)
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        exit_btn = tk.Button(header_frame, text="❌", font=("Arial", 14), bg="red", fg="white",
                             command=self.exit_fullscreen, border=0)
        exit_btn.pack(side="right", padx=20, pady=15)

        # Task Frame
        task_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        task_frame.pack(fill="both", expand=True, padx=50, pady=20)

        self.tasks_listbox = tk.Listbox(task_frame, font=task_font, selectmode=tk.EXTENDED, width=50, height=20, bd=0)
        self.tasks_listbox.pack(fill="both", expand=True, padx=20, pady=20)

        # Load existing tasks from file
        self.load_existing_tasks()

        # Delete Button
        delete_button = tk.Button(self.root, text="🗑 Delete", font=("Arial", 14), bg="white", fg="black",
                                  border=0, command=self.delete_task)
        delete_button.pack(pady=5)

        # Entry and Buttons
        input_frame = tk.Frame(self.root, bg="#EAEAF5")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, font=("Arial", 14), width=40)
        self.task_entry.pack(pady=5)

        add_button = tk.Button(input_frame, text="+ New Task", font=("Arial", 14, "bold"),
                               bg="#A268D3", fg="white", border=0, padx=20, pady=5, width=20,
                               command=self.add_task)
        add_button.pack(pady=5)

        self.edit_button = tk.Button(input_frame, text="✏ Edit Task", font=("Arial", 14, "bold"),
                                     bg="#FFA500", fg="white", border=0, padx=20, pady=5, width=20,
                                     command=self.edit_task, state=tk.DISABLED)
        self.edit_button.pack(pady=5)

        self.task_entry.bind("<Return>", self.add_or_edit_task)
        self.tasks_listbox.bind("<<ListboxSelect>>", self.select_task)
        self.selected_index = None

    def load_existing_tasks(self):
        """Loads tasks from the file into the UI."""
        tasks = file_handler.load_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"• {task}")

    def add_task(self):
        """Adds a task to the list and file."""
        task = self.task_entry.get().strip()
        if task:
            self.tasks_listbox.insert(tk.END, f"• {task}")
            file_handler.save_task(task)  # Save to file
            self.task_entry.delete(0, tk.END)
            self.selected_index = None  
            self.edit_button.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def edit_task(self):
        """Edits a task in the list and updates the file."""
        if self.selected_index is not None:
            updated_task = self.task_entry.get().strip()
            if updated_task:
                self.tasks_listbox.delete(self.selected_index)
                self.tasks_listbox.insert(self.selected_index, f"• {updated_task}")
                file_handler.edit_task(self.selected_index, updated_task)  # Update file
                self.task_entry.delete(0, tk.END)
                self.selected_index = None
                self.edit_button.config(state=tk.DISABLED)
            else:
                messagebox.showwarning("Warning", "Task cannot be empty!")

    def add_or_edit_task(self, event):
        """Handles pressing 'Enter' key to add or edit a task."""
        if self.selected_index is not None:
            self.edit_task()
        else:
            self.add_task()

    def delete_task(self):
        """Deletes selected tasks from UI and file."""
        selected_indices = self.tasks_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No task selected!")
            return

        # Convert to list and remove from highest index to lowest
        indices_to_remove = list(selected_indices)
        for index in reversed(indices_to_remove):
            self.tasks_listbox.delete(index)

        file_handler.delete_tasks(indices_to_remove)  # Remove from file
        self.task_entry.delete(0, tk.END)
        self.selected_index = None
        self.edit_button.config(state=tk.DISABLED)

    def select_task(self, event):
        """Selects a task for editing."""
        try:
            selected_tuple = self.tasks_listbox.curselection()
            if selected_tuple:
                self.selected_index = selected_tuple[0]
                task_text = self.tasks_listbox.get(self.selected_index)[2:]
                self.task_entry.delete(0, tk.END)
                self.task_entry.insert(0, task_text)
                self.edit_button.config(state=tk.NORMAL)
        except IndexError:
            pass

    def exit_fullscreen(self):
        """Exit full-screen mode."""
        self.root.attributes("-fullscreen", False)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
