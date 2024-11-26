import shutil
import tkinter
import tkinter.messagebox

import customtkinter

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


        self.delete_directory_button = customtkinter.CTkButton(
            self.directory_buttons_frame, text='Delete', width=50, fg_color='#636363', hover_color='#3b3b3b',
            image=load_image('icons/delete_folder.png'), command=self.delete
        )
        self.delete_directory_button.pack(side='left')

        self.list_box = tkinter.Listbox(self, selectmode='multiple')
        self.list_box.pack(fill='both', expand=True)

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
                self.list_box.delete(selection)
                self.output_panel.insert('end', f'Deleted {directory}')
            except Exception as error:
                self.output_panel.insert('end', f'Failed to delete "{directory}": {error}')

    def on_created(self, event):
        if event.is_directory:
            self.list_box.insert('end', f"{event.src_path}")