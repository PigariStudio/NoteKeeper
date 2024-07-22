import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class NoteKeeper:
    def __init__(self, root, storage_file='notes.json'):
        self.root = root
        self.storage_file = storage_file
        self.notes = self.load_notes()
        self.root.title("NoteKeeper")

        # Create main frame
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Create Listbox to display notes
        self.listbox = tk.Listbox(self.frame, width=50, height=15)
        self.listbox.pack(side=tk.LEFT, padx=(0, 10))
        self.listbox.bind('<<ListboxSelect>>', self.display_note)

        # Create scrollbar for Listbox
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Create text widget to display note content
        self.text_widget = tk.Text(self.frame, width=50, height=15, wrap=tk.WORD)
        self.text_widget.pack(side=tk.LEFT)

        # Create buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=(10, 0))

        self.add_button = tk.Button(self.button_frame, text="Add Note", command=self.add_note)
        self.add_button.pack(side=tk.LEFT, padx=(0, 10))

        self.edit_button = tk.Button(self.button_frame, text="Edit Note", command=self.edit_note)
        self.edit_button.pack(side=tk.LEFT, padx=(0, 10))

        self.delete_button = tk.Button(self.button_frame, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(side=tk.LEFT, padx=(0, 10))

        self.load_listbox()

    def load_notes(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        return []

    def save_notes(self):
        with open(self.storage_file, 'w') as file:
            json.dump(self.notes, file, indent=4)

    def load_listbox(self):
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            self.listbox.insert(tk.END, note['title'])

    def add_note(self):
        title = simpledialog.askstring("Add Note", "Enter note title:")
        if title:
            content = simpledialog.askstring("Add Note", "Enter note content:")
            if content:
                self.notes.append({'title': title, 'content': content})
                self.save_notes()
                self.load_listbox()

    def display_note(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            note = self.notes[index]
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, note['content'])

    def edit_note(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            note = self.notes[index]
            new_title = simpledialog.askstring("Edit Note", "Edit title:", initialvalue=note['title'])
            new_content = simpledialog.askstring("Edit Note", "Edit content:", initialvalue=note['content'])
            if new_title and new_content:
                self.notes[index] = {'title': new_title, 'content': new_content}
                self.save_notes()
                self.load_listbox()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, new_content)

    def delete_note(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?"):
                self.notes.pop(index)
                self.save_notes()
                self.load_listbox()
                self.text_widget.delete(1.0, tk.END)


root = tk.Tk()
app = NoteKeeper(root)
root.mainloop()
