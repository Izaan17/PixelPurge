import os
import tkinter.messagebox
from tkinter import filedialog

import customtkinter

from widgets.buttons.directory_button import DirectoryButton
from utils.loader import load_image


class DirectoryPopup(customtkinter.CTkToplevel):
    """
    Popup for selecting and adding a directory with an optional recursive flag.
    """

    def __init__(self, parent, on_add_callback):
        """
        Initializes the popup.

        Args:
            parent: The parent window.
            on_add_callback: Callback to invoke when the "Add" button is pressed,
                             passing the selected directory and recursive state.
        """
        super().__init__(parent)
        self.on_add_callback = on_add_callback

        # Set up modal behavior
        self.transient(parent)
        self.grab_set()
        self.title("Add Directory")
        self.minsize(500, 200)
        self.resizable(False, False)

        # Input variables
        self.directory_var = customtkinter.StringVar()
        self.recursive_var = customtkinter.BooleanVar(value=False)

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the widgets for the popup.
        """
        file_widgets_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        file_widgets_frame.pack()


        # Entry for directory
        directory_entry = customtkinter.CTkEntry(file_widgets_frame,
                                                 width=400,
                                                 textvariable=self.directory_var)
        directory_entry.pack(pady=10, padx=10, side='left')


        # Button to open file dialog
        file_selector_button = DirectoryButton(
            file_widgets_frame,
            width=10,
            height=10,
            text='',
            command=self.open_directory_selector,
            image=load_image('icons/folder.png', (20, 20))
        )
        file_selector_button.pack(pady=10)

        metadata_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        metadata_frame.pack(padx=30, pady=5, fill='both')

        # Checkbox for recursive option
        recursive_checkbox = customtkinter.CTkCheckBox(
            metadata_frame,
            text="Recursive",
            variable=self.recursive_var
        )
        recursive_checkbox.grid(column=0, row=0)

        # Frame for action buttons
        button_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        button_frame.pack(pady=10, side='bottom')

        # Cancel button
        cancel_button = DirectoryButton(
            button_frame,
            text='Cancel',
            command=self.destroy,
            width=140
        )
        cancel_button.pack(side='left', padx=(5, 20))

        # Add button
        add_button = DirectoryButton(
            button_frame,
            text='Add',
            command=self.handle_add,
            width=140
        )
        add_button.pack(side='left', padx=(20, 5))

    def open_directory_selector(self):
        """
        Opens a directory selection dialog.
        """
        selected_directory = filedialog.askdirectory(mustexist=True)
        if selected_directory:
            self.directory_var.set(selected_directory)

    def handle_add(self):
        """
        Validates the input and invokes the callback if valid.
        """
        directory = self.directory_var.get()
        recursive = self.recursive_var.get()

        if not directory:
            tkinter.messagebox.showerror('Add Directory', 'No directory selected.')
            return

        if not os.path.exists(directory):
            tkinter.messagebox.showerror('Add Directory', 'Directory does not exist.')
            return

        # Pass the directory and recursive option to the callback
        self.on_add_callback(directory, recursive)
        self.destroy()
