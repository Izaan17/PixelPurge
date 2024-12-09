import os
import tkinter.messagebox
from tkinter import filedialog

import customtkinter

from utils.loader import load_icon
from widgets.buttons.directory_button import DirectoryButton
from widgets.checkboxes.check_box import DefaultCheckBox


class DirectoryPopup(customtkinter.CTkToplevel):
    """
    Popup for selecting and adding or editing a directory with an optional recursive flag.
    """

    def __init__(self, parent, on_submit_callback, directory=None, recursive=False, edit_mode=False):
        """
        Initializes the popup for either adding or editing a directory.

        Args:
            parent: The parent window.
            on_submit_callback: Callback to invoke when the "Add" or "Save" button is pressed. Passes 3 parameters: directory, recursive, and edit mode status
            directory: The directory to pre-populate if editing (default is None).
            recursive: The recursive state to pre-populate if editing (default is False).
            edit_mode: Boolean indicating if we're editing an existing directory.
        """
        super().__init__(parent)
        self.on_submit_callback = on_submit_callback
        self.edit_mode = edit_mode
        self.original_directory = directory  # Store original directory for edit mode

        # Set up modal behavior
        self.transient(parent)
        self.grab_set()
        self.title("Edit Directory" if edit_mode else "Add Directory")
        self.minsize(500, 200)
        self.resizable(False, False)

        # Input variables
        self.directory_var = customtkinter.StringVar(value=directory or "")
        self.recursive_var = customtkinter.BooleanVar(value=recursive)

        # Create UI Components
        self.create_widgets()

        # Center the popup
        self.center_window()

        # Bind escape key to close
        self.bind("<Escape>", lambda e: self.destroy())

    def center_window(self):
        """Centers the popup window relative to its parent."""
        self.update_idletasks()
        parent = self.master
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        """Creates the widgets for the popup with improved layout and feedback."""
        # Main container with padding
        main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Directory selection frame
        file_widgets_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        file_widgets_frame.pack(fill="x")

        # Label for directory
        dir_label = customtkinter.CTkLabel(file_widgets_frame, text="Directory Path:")
        dir_label.pack(anchor="w", padx=5, pady=(0, 5))

        # Directory selection controls
        selection_frame = customtkinter.CTkFrame(file_widgets_frame, fg_color="transparent")
        selection_frame.pack(fill="x")

        # Entry for directory
        self.directory_entry = customtkinter.CTkEntry(
            selection_frame,
            textvariable=self.directory_var,
            placeholder_text="Select a directory..."
        )
        self.directory_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Button to open file dialog
        file_selector_button = DirectoryButton(
            selection_frame,
            width=30,
            height=30,
            text="",
            command=self.open_directory_selector,
            image=load_icon("folder.png", (20, 20))
        )
        file_selector_button.pack(side="right")

        # Options frame
        options_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        options_frame.pack(fill="x", pady=20)

        # Checkbox for recursive option
        self.recursive_checkbox = DefaultCheckBox(
            options_frame,
            text="Include subdirectories (recursive)",
            variable=self.recursive_var,
            corner_radius=6
        )
        self.recursive_checkbox.pack(anchor="w")

        # Buttons frame
        button_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", pady=(20, 0))

        # Cancel button
        cancel_button = DirectoryButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=140,
            fg_color=("gray75", "gray30")
        )
        cancel_button.pack(side="left")

        # Add/Save button
        action_text = "Save Changes" if self.edit_mode else "Add Directory"
        self.action_button = DirectoryButton(
            button_frame,
            text=action_text,
            command=self.handle_submit,
            width=140
        )
        self.action_button.pack(side="right")

    def open_directory_selector(self):
        """Opens a directory selection dialog with improved feedback."""
        initial_dir = self.directory_var.get() if os.path.exists(self.directory_var.get()) else os.path.expanduser("~")
        selected_directory = filedialog.askdirectory(
            initialdir=initial_dir,
            title="Select Directory",
            mustexist=True
        )
        if selected_directory:
            self.directory_var.set(selected_directory)

    @staticmethod
    def validate_directory(directory):
        """
        Validates the selected directory.

        Returns:
            tuple: (is_valid, error_message)
        """
        if not directory:
            return False, "No directory selected."

        if not os.path.exists(directory):
            return False, "Selected directory does not exist."

        if not os.path.isdir(directory):
            return False, "Selected path is not a directory."

        return True, None

    def handle_submit(self):
        """Validates the input and invokes the callback if valid."""
        directory = self.directory_var.get().strip()
        recursive = self.recursive_var.get()

        # Validate directory
        is_valid, error_message = self.validate_directory(directory)
        if not is_valid:
            tkinter.messagebox.showerror("Invalid Directory", error_message)
            return

        # In edit mode, check if anything changed
        if self.edit_mode and directory == self.original_directory:
            # If only recursive flag changed, that's fine, continue
            pass

        try:
            # Pass the directory, recursive option, and edit_mode to the callback
            self.on_submit_callback(directory, recursive, self.edit_mode)
            self.destroy()
        except Exception as e:
            tkinter.messagebox.showerror(
                "Error",
                f"Failed to {'update' if self.edit_mode else 'add'} directory:\n{str(e)}"
            )
