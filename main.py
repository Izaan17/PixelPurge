import customtkinter

from watcher import PixelWatcher
from widgets.control_panel import ControlPanel
from widgets.directory_list_box import DirectoryListBox
from widgets.directory_list_tree_box import DirectoryListTreeBox
from widgets.output_panel import OutputPanel


class PixelPurge(customtkinter.CTk):
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('PixelPurge')
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')
        self.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.iconbitmap('icons/pixel.ico')

        # Pixel watcher handles events when new folders are created
        self.pixel_watcher = PixelWatcher()

        # App Label
        self.app_label = customtkinter.CTkLabel(self, text='PixelPurge', font=('', 18, 'bold'))
        self.app_label.pack(pady=10)

        self.directory_info_frame = customtkinter.CTkFrame(self)
        self.directory_info_frame.pack(fill='both', expand=True, padx=20)

        self.output_panel = OutputPanel(self)

        # Directory Widget
        self.directory_tree_view = DirectoryListTreeBox(self.directory_info_frame, fg_color='transparent')
        self.directory_tree_view.pack(side='left', fill="both", expand=True, padx=10, pady=10)

        self.directory_results_list_box = DirectoryListBox(self.directory_info_frame, self.pixel_watcher,
                                                           self.output_panel, fg_color='transparent')
        self.directory_results_list_box.pack(side='right', fill="both", expand=True, padx=10, pady=10)

        # Load saved directories on startup
        self.directory_tree_view.load()

        self.output_panel.pack(padx=20, pady=(10, 10), fill='x')

        # Controls Panel
        self.controls_panel = ControlPanel(self, self.directory_tree_view, self.output_panel, self.pixel_watcher)
        self.controls_panel.pack(side='left', pady=(0, 10), padx=20)


if __name__ == '__main__':
    app = PixelPurge()
    app.mainloop()
