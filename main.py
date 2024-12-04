import customtkinter

from utils.loader import load_image
from watcher import PixelWatcher
from widgets.buttons.toggle_icon_button import ToggleIconButton
from widgets.control_panel import ControlPanel
from widgets.directory_list_box import DirectoryListBox
from widgets.directory_list_tree_box import DirectoryListTreeBox
from widgets.output_panel import OutputPanel


class PixelPurge(customtkinter.CTk):
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 750

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('PixelPurge')
        self.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.iconbitmap('icons/pixel.ico')
        self.configure(fg_color=('white', '#0d1b2a'))

        # Pixel watcher handles events when new folders are created
        self.pixel_watcher = PixelWatcher()

        self.app_bar = customtkinter.CTkFrame(self, fg_color='transparent')
        self.app_bar.pack(fill='x')

        # App Label
        self.app_label = customtkinter.CTkLabel(self.app_bar, text='PixelPurge', font=('', 18, 'bold'),
                                                text_color=('black', 'white'))
        self.app_label.pack(padx=30, pady=10, side='left')

        self.toggle_appearance_button = ToggleIconButton(self.app_bar, text='',
                                                                command=self.toggle_appearance_mode,
                                                                corner_radius=20,
                                                                width=30,
                                                                fg_color=('#E5E7EB', '#334155'),
                                                                hover_color=('#D1D5DB', '#475569'),
                                                                first_image=load_image('icons/sun.png'),
                                                                second_image=load_image('icons/moon.png'),
                                                                initial_state=1 if customtkinter.get_appearance_mode() == 'Light' else 0
                                                         )
        self.toggle_appearance_button.pack(side='right', padx=30)

        self.directory_info_frame = customtkinter.CTkFrame(self, fg_color=('#F9FAFB', '#1E293B'))
        self.directory_info_frame.pack(fill='both', expand=True, padx=20)

        self.output_panel = OutputPanel(self, fg_color=('#F9FAFB', '#1E293B'))

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

    @staticmethod
    def toggle_appearance_mode():
        current_mode = customtkinter.get_appearance_mode()
        new_mode = 'Dark' if current_mode == 'Light' else 'Light'
        customtkinter.set_appearance_mode(new_mode)

if __name__ == '__main__':
    app = PixelPurge()
    app.mainloop()
