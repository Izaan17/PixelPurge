import customtkinter
from watcher import PixelMonitor, PixelWatcher
from widgets.directory_list_tree_box import DirectoryListTreeBox
from widgets.output_panel import OutputPanel
from widgets.buttons.toggle_button import ToggleButton

class ControlPanel(customtkinter.CTkFrame):
    def __init__(self, master, directory_list_box: DirectoryListTreeBox, output_panel: OutputPanel, pixel_watcher: PixelWatcher, **kwargs):
        super().__init__(master, **kwargs)

        self.directory_list_box = directory_list_box
        self.output_panel = output_panel
        self.pixel_watcher = pixel_watcher  # Use the passed PixelWatcher instance
        self.pixel_watcher.add_callback(self.on_created)  # Register the on_created callback
        self.pixel_monitor = PixelMonitor(self.pixel_watcher)

        # ToggleButton for Start/Stop functionality
        self.start_button = ToggleButton(
            self,
            text_on="Stop",
            text_off="Start",
            colors_on=("red", "darkred"),
            colors_off=("green", "darkgreen"),
            hover_colors_on=("darkred", "maroon"),
            hover_colors_off=("darkgreen", "forestgreen"),
            command_on=self.start,
            command_off=self.stop,
            initial_state=False,
            corner_radius=5
        )
        self.start_button.pack(side='left', padx=(0, 10))

        # Clear button
        self.clear_button = customtkinter.CTkButton(self, text='Clear', corner_radius=5, fg_color='#393e46',
                                                    hover_color='#606470', command=self.output_panel.clear)
        self.clear_button.pack()

    def start(self):
        """
        Start monitoring directories.
        """
        self.output_panel.insert('end', '[Monitoring]:')
        directories_to_monitor = self.directory_list_box.get_directories()
        for directory, data in directories_to_monitor.items():
            self.output_panel.insert('end', f'{directory:<100}')
            self.output_panel.insert('end', f'Recursive: {data["recursive"]}\n')
            self.pixel_monitor.monitor_folder(directory, data['recursive'])

        self.pixel_monitor.start()
        self.output_panel.insert('end', '[STATUS] Started.')

    def stop(self):
        """
        Stop monitoring directories.
        """
        self.output_panel.insert('end', '[STATUS] Stopped.')
        self.pixel_monitor.stop()

    def on_created(self, event):
        """
        Callback to handle new directories created.
        """
        if event.is_directory:
            self.output_panel.insert('end', f"New directory: {event.src_path}")
