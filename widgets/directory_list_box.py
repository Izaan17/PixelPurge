import shutil
import tkinter
import tkinter.messagebox

import customtkinter

from widgets.buttons.directory_button import DirectoryButton
from utils.loader import load_image
from watcher import PixelWatcher
from widgets.output_panel import OutputPanel


class DirectoryListBox(customtkinter.CTkFrame):
    def __init__(self, master, pixel_watcher: PixelWatcher, output_panel: OutputPanel, **kwargs):
        super().__init__(master, **kwargs)

        self.output_panel = output_panel
        self.pixel_watcher = pixel_watcher
        self.pixel_watcher.add_callback(self.on_created)

        # Buttons Frame
        self.directory_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.directory_buttons_frame.pack(fill='x', padx=0, pady=10)

        # Select all button
        self.select_all_button = DirectoryButton(
            self.directory_buttons_frame, text='Select All', image=load_image('icons/folder.png'),
            command=self.select_all)

        self.select_all_button.pack(side='left', padx=(0, 10))

        self.delete_directory_button = DirectoryButton(
            self.directory_buttons_frame, text='Delete', image=load_image('icons/delete_folder.png'),
            command=self.delete)
        self.delete_directory_button.pack(side='left')

        self.list_box = tkinter.Listbox(self, selectmode='multiple')
        self.list_box.pack(fill='both', expand=True)

    def select_all(self):
        self.list_box.selection_set(0, 'end')

    def delete(self):
        # reverse to prevent shifting
        selections = self.list_box.curselection()[::-1]

        if not selections:
            return

        if not tkinter.messagebox.askyesno('Delete Folders', f'Are you sure you want to {len(selections)} folders?'):
            return

        for selection in selections:
            directory = self.list_box.get(selection)
            try:
                shutil.rmtree(directory)
                self.output_panel.insert('end', f'Deleted {directory}')
            except Exception as error:
                self.output_panel.insert('end', f'Failed to delete "{directory}": {error}')
            self.list_box.delete(selection)
    def on_created(self, event):
        if event.is_directory:
            self.list_box.insert('end', f"{event.src_path}")