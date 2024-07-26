import tkinter as tk
from tkinter import filedialog
import os
from fileorganizer import FileOrganizer
from apicaller import APIcall

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        self.label = tk.Label(root, text="Select files to organize:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Add Files", command=self.add_files)
        self.select_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Clear Files", command=self.clear_files)
        self.clear_button.pack(pady=5)

        self.organize_button = tk.Button(root, text="Organize Files", command=self.organize_files, state=tk.DISABLED)
        self.organize_button.pack(pady=5)

        self.upload_button = tk.Button(root, text="Upload to Google Drive", command=self.upload_to_drive, state=tk.DISABLED)
        self.upload_button.pack(pady=5)

        self.organize_and_upload_button = tk.Button(root, text="Organize and Upload", command=self.organize_and_upload, state=tk.DISABLED)
        self.organize_and_upload_button.pack(pady=5)

        self.preview_button = tk.Button(root, text="Preview Organization", command=self.preview_organization, state=tk.DISABLED)
        self.preview_button.pack(pady=5)

        self.file_listbox = tk.Listbox(root, height=10, width=50)
        self.file_listbox.pack(pady=10)

        self.selected_files = []

    def add_files(self):
        new_files = filedialog.askopenfilenames(title="Select Files")
        if new_files:
            self.selected_files.extend(new_files)
            self.file_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.file_listbox.insert(tk.END, file)
            self.organize_button.config(state=tk.NORMAL)
            self.upload_button.config(state=tk.NORMAL)
            self.organize_and_upload_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)

    def clear_files(self):
        self.selected_files = []
        self.file_listbox.delete(0, tk.END)
        self.organize_button.config(state=tk.DISABLED)
        self.upload_button.config(state=tk.DISABLED)
        self.organize_and_upload_button.config(state=tk.DISABLED)
        self.preview_button.config(state=tk.DISABLED)

    def preview_organization(self):
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Preview Organization")
        preview_listbox = tk.Listbox(self.preview_window, height=10, width=50)
        preview_listbox.pack(pady=10)

        for file in self.selected_files:
            directory = os.path.dirname(file)
            organizer = FileOrganizer(directory)
            organized_files = organizer.preview_organization()  
            for organized_file in organized_files:
                preview_listbox.insert(tk.END, organized_file)

        confirm_button = tk.Button(self.preview_window, text="Confirm", command=self.confirm_organization)
        confirm_button.pack(pady=5)

    def confirm_organization(self):
        self.preview_window.destroy()
        self.organize_files()

    def organize_files(self):
        organized_folders = set()
        for file in self.selected_files:
            directory = os.path.dirname(file)
            organizer = FileOrganizer(directory)
            organized_folder = organizer.organize_files()
            organized_folders.add(organized_folder)
        return organized_folders

    def organize_and_upload(self):
        organized_folders = self.organize_files()
        self.upload_to_drive(organized_folders)

    def upload_to_drive(self, folders=None):
        if folders is None:
            folders = {os.path.dirname(file) for file in self.selected_files}
        for folder in folders:
            api_caller = APIcall(folder)
            api_caller.upload_file()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()