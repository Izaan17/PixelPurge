import json
import os.path
import tkinter.messagebox
from tkinter import messagebox, ttk

import customtkinter

import constants
from utils.loader import load_image
from widgets.buttons.directory_button import DirectoryButton
from widgets.directory_popup import DirectoryPopup


class DirectoryListTreeBox(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.directories_metadata = {}
        self._setup_ui()
        self._configure_treeview_style()

    def _setup_ui(self):
        # Buttons Frame
        self.directory_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.directory_buttons_frame.pack(fill='x', pady=10)

        # Create buttons with consistent spacing
        buttons_config = [
            ('Add', 'icons/add_folder.png', self.make_directory, 0),
            ('Add default directories', 'icons/add_folder.png', self.add_default_directories, 10),
            ('Delete', 'icons/delete_folder.png', self.delete_directory, 10)
        ]

        for text, icon, command, padx in buttons_config:
            button = DirectoryButton(
                self.directory_buttons_frame,
                text=text,
                image=load_image(icon),
                command=command,
            )
            button.pack(side='left', padx=(padx, 0))
            if text == 'Delete':
                button.configure(fg_color='#DC2626', hover_color='#B91C1C')

        # Treeview Frame
        self.tree_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.tree_frame.pack(fill='both', expand=True)

        # Create Treeview
        self.tree = ttk.Treeview(self.tree_frame, show='headings')
        self.tree['columns'] = ('directory', 'recursive')

        # Configure columns
        self.tree.column('directory', width=300, stretch=True)
        self.tree.column('recursive', width=100, anchor='center', stretch=False)

        # Configure headers
        self.tree.heading('directory', text='Directory', anchor='w')
        self.tree.heading('recursive', text='Recursive', anchor='center')

        # Pack widgets
        self.tree.pack(side='left', fill='both', expand=True)

        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)

    @staticmethod
    def _configure_treeview_style():
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        colors = {
            'bg': '#2b2b2b',
            'fg': 'white',
            'selected_bg': '#4f4f4f',
            'alternate_bg': '#333333'
        }

        # Apply styles
        style.configure('Treeview',
                        background=colors['bg'],
                        foreground=colors['fg'],
                        fieldbackground=colors['bg'],
                        borderwidth=0,
                        relief='flat',
                        rowheight=30)

        style.map('Treeview',
                  background=[('selected', colors['selected_bg'])],
                  foreground=[('selected', colors['fg'])])

        # Configure header style
        style.configure('Treeview.Heading',
                        background=colors['bg'],
                        foreground=colors['fg'],
                        relief='flat')

        style.map('Treeview.Heading',
                  background=[('active', colors['selected_bg'])])

    def on_add(self, directory, recursive):
        """Callback for when a directory is added."""
        if not directory:
            return

        if directory in self.directories_metadata:
            messagebox.showerror('Error', 'Directory already exists')
            return

        self.add_directory(directory, {'recursive': recursive})

    def make_directory(self):
        """Opens directory selection popup."""
        DirectoryPopup(self, self.on_add)

    def add_directory(self, directory, metadata):
        """Adds a directory with metadata to the treeview."""
        if directory in self.directories_metadata or not os.path.exists(directory):
            return False

        self.directories_metadata[directory] = metadata
        self.tree.insert('', 'end',
                         values=(directory, 'Yes' if metadata['recursive'] else 'No'))
        self.save()
        return True

    def edit_directory(self, directory, metadata):
        """Updates directory metadata and refreshes display."""
        if directory not in self.directories_metadata:
            return False

        self.directories_metadata[directory] = metadata

        # Update display
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == directory:
                self.tree.item(item,
                               values=(directory, 'Yes' if metadata['recursive'] else 'No'))
                break

        self.save()
        return True

    def add_default_directories(self):
        """Adds predefined default directories."""
        for directory in constants.DEFAULT_DIRECTORIES:
            if not self.add_directory(directory, {'recursive': True}):
                tkinter.messagebox.showerror('Default Directories', f'Failed to add directory: {directory}')

    def delete_directory(self):
        """Deletes selected directory entries."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror('Error', 'Please select a directory to delete')
            return

        if messagebox.askyesno('Confirm Delete',
                               'Are you sure you want to delete the selected directories?'):
            for item in selected:
                directory = self.tree.item(item)['values'][0]
                del self.directories_metadata[directory]
                self.tree.delete(item)
            self.save()

    def clear(self):
        """Removes all entries."""
        self.tree.delete(*self.tree.get_children())
        self.directories_metadata.clear()
        self.save()

    def save(self):
        """Saves directory metadata to file."""
        try:
            os.makedirs(constants.PIXEL_PURGE_FOLDER, exist_ok=True)
            with open(constants.PIXEL_PURGE_DIRECTORIES_FILE, 'w') as fp:
                json.dump(self.directories_metadata, fp, indent=4)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save directories: {str(e)}')

    def load(self):
        """Loads directory metadata from file."""
        if not os.path.exists(constants.PIXEL_PURGE_DIRECTORIES_FILE):
            return
        invalid_directories = []
        try:
            with open(constants.PIXEL_PURGE_DIRECTORIES_FILE, 'r') as fp:
                self.directories_metadata = json.load(fp)

            for directory, metadata in self.directories_metadata.items():
                if not os.path.exists(directory):
                    invalid_directories.append(directory)
                    continue
                self.tree.insert('', 'end',
                                 values=(directory, 'Yes' if metadata['recursive'] else 'No'))
            if invalid_directories:
                tkinter.messagebox.showinfo('Invalid Directories Detected', f'Invalid directories have been detected: {invalid_directories}')
            for invalid_dir in invalid_directories:
                del self.directories_metadata[invalid_dir]
            self.save()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load directories: {str(e)}')

    def get_directories(self):
        """Returns the current directory metadata dictionary."""
        return self.directories_metadata

    def on_double_click(self, event):
        """Handles double-click editing of entries."""
        region = self.tree.identify_region(event.x, event.y)
        if region != 'cell':
            return

        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected)['values']
        if not values:
            return

        directory = values[0]
        metadata = self.directories_metadata.get(directory)
        if metadata:
            DirectoryPopup(self,
                           on_add_callback=lambda d, r: self.edit_directory(d, {'recursive': r}),
                           directory=directory,
                           recursive=metadata['recursive'])
