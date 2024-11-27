import os
import shutil
import tkinter as tk
from tkinter import messagebox

import customtkinter

from utils.loader import load_image
from watcher import PixelWatcher
from widgets.buttons.directory_button import DirectoryButton
from widgets.output_panel import OutputPanel


class DirectoryListBox(customtkinter.CTkFrame):
    def __init__(self, master, pixel_watcher: PixelWatcher, output_panel: OutputPanel, **kwargs):
        super().__init__(master, **kwargs)

        self.output_panel = output_panel
        self.pixel_watcher = pixel_watcher
        self.pixel_watcher.add_callback(self.on_created)

        self._setup_ui()

    def _setup_ui(self):
        """Initialize and configure UI components."""
        # Buttons Frame
        self.directory_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.directory_buttons_frame.pack(fill='x', padx=0, pady=10)

        # Create buttons
        buttons_config = [
            ('Select All', 'icons/folder.png', self.select_all, 0),
            ('Delete', 'icons/delete_folder.png', self.delete, 10)
        ]

        for text, icon, command, padx in buttons_config:
            button = DirectoryButton(
                self.directory_buttons_frame,
                text=text,
                image=load_image(icon),
                command=command
            )
            button.pack(side='left', padx=(padx, 0))

        # Create frame for listbox and scrollbar
        self.list_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.list_frame.pack(fill='both', expand=True)

        # Create and configure listbox
        self.list_box = tk.Listbox(
            self.list_frame,
            selectmode='multiple',
            bg='#2b2b2b',
            fg='white',
            selectbackground='#4f4f4f',
            selectforeground='white',
            activestyle="none",
            relief="flat",
            borderwidth=0,
            font=('TkDefaultFont', 10)
        )

        # Pack listbox and scrollbar
        self.list_box.pack(side='left', fill='both', expand=True)

        # Bind events
        self.list_box.bind('<Delete>', lambda e: self.delete())
        self.list_box.bind('<Control-a>', self.select_all_shortcut)


    def select_all(self):
        """Select all items in the listbox."""
        self.list_box.selection_clear(0, tk.END)
        self.list_box.selection_set(0, tk.END)

    def select_all_shortcut(self, _):
        """Handle Ctrl+A keyboard shortcut."""
        self.select_all()
        return 'break'  # Prevent default behavior

    def delete(self):
        """Delete selected directories."""
        selections = list(self.list_box.curselection())[::-1]  # Reverse for safe deletion

        if not selections:
            messagebox.showinfo('Delete Folders', 'Please select folders to delete')
            return

        folder_count = len(selections)
        if not messagebox.askyesno('Delete Folders',
                                   f'Are you sure you want to delete {folder_count} folder{"s" if folder_count > 1 else ""}?\n\n'
                                   'This action cannot be undone.'):
            return

        deleted_count = 0
        for index in selections:
            directory = self.list_box.get(index)
            if self._delete_directory(directory):
                self.list_box.delete(index)
                deleted_count += 1

        self._show_deletion_results(deleted_count, folder_count)

    def _delete_directory(self, directory: str) -> bool:
        """
        Attempt to delete a directory and log the result.

        Args:
            directory: Path to directory to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            if not os.path.exists(directory):
                self.output_panel.insert('end', f'Directory not found: {directory}')
                return True  # Return True to remove from list

            shutil.rmtree(directory)
            self.output_panel.insert('end', f'Successfully deleted: {directory}')
            return True

        except PermissionError:
            self.output_panel.insert('end', f'Permission denied: {directory}')
        except Exception as error:
            self.output_panel.insert('end', f'Failed to delete "{directory}": {str(error)}')

        return False

    @staticmethod
    def _show_deletion_results(deleted_count: int, total_count: int):
        """Show result message after batch deletion."""
        if deleted_count == total_count:
            if total_count == 1:
                messagebox.showinfo('Success', 'Folder was successfully deleted')
            else:
                messagebox.showinfo('Success', f'All {total_count} folders were successfully deleted')
        else:
            messagebox.showwarning('Warning',
                                   f'Deleted {deleted_count} out of {total_count} folders.\n'
                                   'Check the output panel for details.')

    def on_created(self, event):
        """Handle directory creation events."""
        if not event.is_directory:
            return

        # Ensure path exists and is a directory
        if not os.path.exists(event.src_path) or not os.path.isdir(event.src_path):
            return

        # Add to listbox if not already present
        path = str(event.src_path)
        existing_items = self.list_box.get(0, tk.END)
        if path not in existing_items:
            self.list_box.insert(tk.END, path)
            self.output_panel.insert('end', f'Added new directory: {path}')

    def clear(self):
        """Clear all items from the listbox."""
        self.list_box.delete(0, tk.END)