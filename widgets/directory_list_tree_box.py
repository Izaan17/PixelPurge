import json
import os.path
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter
from utils.loader import load_image
from widgets.directory_popup import DirectoryPopup
import constants

class DirectoryListTreeBox(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.directories_metadata = {}  # Stores metadata for each directory


        # Buttons Frame
        self.directory_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.directory_buttons_frame.pack(fill='x', pady=10)

        self.add_directory_button = customtkinter.CTkButton(
            self.directory_buttons_frame, text='Add', width=50, fg_color='#636363',
            hover_color='#3b3b3b', image=load_image('icons/add_folder.png'), command=self.make_directory
        )
        self.add_directory_button.pack(side='left')

        self.delete_directory_button = customtkinter.CTkButton(
            self.directory_buttons_frame, text='Delete', width=50, fg_color='#636363', hover_color='#3b3b3b',
            image=load_image('icons/delete_folder.png'), command=self.delete_directory
        )
        self.delete_directory_button.pack(side='left', padx=10)

        # Treeview Frame
        self.tree_frame = customtkinter.CTkFrame(self)
        self.tree_frame.pack(fill='both', expand=True)

        # Treeview Widget
        self.tree = ttk.Treeview(self.tree_frame, show='headings')
        self.tree['columns'] = ('directory', 'recursive')
        self.tree.column('directory')
        self.tree.column('recursive', anchor='c')

        self.tree.heading('directory', text='Directory')
        self.tree.heading('recursive', text='Recursive')

        self.tree.pack(fill='both', expand=True)

    def make_directory(self):
        """
        Opens a popup to allow the user to add a directory with a recursive option.
        """
        def on_add(directory, recursive):
            """
            Callback for when a directory is added.
            """
            if directory in self.directories_metadata:
                messagebox.showerror('Add Directory', 'Directory already exists.')
                return

            # Add the directory with the specified recursive metadata
            metadata = {'recursive': recursive}
            self.add_directory(directory, metadata)

        # Create and show the popup
        DirectoryPopup(self, on_add)

    def add_directory(self, directory, metadata):
        """
        Adds the given directory to the internal metadata and updates the Treeview.
        """
        self.directories_metadata[directory] = metadata
        self.tree.insert('', 'end', text=directory, values=(directory, metadata['recursive']))
        self.save()

    def delete_directory(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return messagebox.showerror('Delete Directory', 'Please select a directory to delete.')

        for item in selected_item:
            # Remove from Treeview and metadata storage
            directory = self.tree.item(item, 'text')  # Get directory path from Treeview
            del self.directories_metadata[directory]
            self.tree.delete(item)

        self.save()

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def edit_metadata(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return messagebox.showerror('Edit Metadata', 'Please select a directory to edit.')

        directory = self.tree.item(selected_item[0], 'text')  # Get directory path
        metadata = self.directories_metadata[directory]

        # Create a pop-up for editing metadata
        edit_window = tk.Toplevel(self)
        edit_window.title('Edit Metadata')
        edit_window.geometry('300x150')

        tk.Label(edit_window, text='Recursive:').pack(pady=10)
        recursive_var = tk.BooleanVar(value=metadata['recursive'])
        tk.Checkbutton(edit_window, text='Enable', variable=recursive_var).pack()

        def save_metadata():
            metadata['recursive'] = recursive_var.get()
            self.directories_metadata[directory] = metadata
            # Update the Treeview
            self.tree.item(selected_item[0], values=(metadata['recursive'],))
            edit_window.destroy()

        tk.Button(edit_window, text='Save', command=save_metadata).pack(pady=20)

    def save(self):
        """
        Saves the current directories and metadata to a JSON file.
        """
        try:
            if not os.path.exists(constants.PIXEL_PURGE_FOLDER):
                os.mkdir(constants.PIXEL_PURGE_FOLDER)

            with open(constants.PIXEL_PURGE_DIRECTORIES_FILE, 'w') as fp:
                json.dump(self.directories_metadata, fp, indent=4)
        except Exception as e:
            messagebox.showerror('Save Error', f"Error saving data: {e}")

    def load(self):
        """
        Loads the directories and metadata from a JSON file.
        """
        if os.path.exists(constants.PIXEL_PURGE_DIRECTORIES_FILE):
            try:
                with open('directories.json', 'r') as fp:
                    self.directories_metadata = json.load(fp)

                # Populate the Treeview with saved data
                for directory, metadata in self.directories_metadata.items():
                    self.tree.insert('', 'end', text=directory, values=(directory, metadata['recursive']))

            except Exception as e:
                messagebox.showerror('Load Error', f"Error loading data: {e}")

    def get_directories(self):
        return self.directories_metadata