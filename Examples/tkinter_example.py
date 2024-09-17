import tkinter as tk
from tkinter import ttk, messagebox
from contextualhelp import ContextualHelp

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tkinter Todo List")
        self.master.geometry("380x400")

        self.tasks = []

        self.create_widgets()
        #Add a help file to use
        self.help_system = ContextualHelp("tkinter_todo_help.ftxt")

        self.create_widgets()

        # Bind F1 key to show help
        self.master.bind_all('<F1>', self.show_help)

    #Define this function to show contextual help
    #You can simply remove the debug print statements
    def show_help(self, event):
        focused_widget = self.master.focus_get()
        if focused_widget:
            element_id = focused_widget.winfo_name()
            print(f"Focused widget: {focused_widget}, Element ID: {element_id}")  # Debug print
  
            help_content = self.help_system.display_help(element_id, "tkinter")
            print(f"Help content: {help_content}")  # Debug print
            if help_content:
                self.display_help_window(help_content)
            else:
                print(f"No help content found for {element_id}")
        else:
            print("No widget focused")

    def create_widgets(self):
        # Task entry
        self.task_entry = ttk.Entry(self.master, width=30, name="task_entry")
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)

        # Add task button
        self.add_button = ttk.Button(self.master, text="Add Task", command=self.add_task, name="add_button")
        self.add_button.grid(row=0, column=1, padx=5, pady=5)

        # Task listbox
        self.task_listbox = tk.Listbox(self.master, width=40, height=15, name="task_listbox")
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Remove task button
        self.remove_button = ttk.Button(self.master, text="Remove Task", command=self.remove_task, name="remove_button")
        self.remove_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(task_index)
            self.tasks.pop(task_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
