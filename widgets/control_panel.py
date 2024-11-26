import customtkinter
from watcher import PixelMonitor, PixelWatcher
from widgets.directory_list_tree_box import DirectoryListTreeBox
from widgets.output_panel import OutputPanel

class ControlPanel(customtkinter.CTkFrame):
    def __init__(self, master, directory_list_box: DirectoryListTreeBox, output_panel: OutputPanel, pixel_watcher: PixelWatcher, **kwargs):
        super().__init__(master, **kwargs)

        self.directory_list_box = directory_list_box
        self.output_panel = output_panel
        self.pixel_watcher = pixel_watcher  # Use the passed PixelWatcher instance
        self.pixel_watcher.add_callback(self.on_created)  # Register the on_created callback
        self.pixel_monitor = PixelMonitor(self.pixel_watcher)

        self.status_text_var = customtkinter.StringVar(value='Start')
        self.status_var = customtkinter.BooleanVar()
        self.start_button = customtkinter.CTkButton(self, textvariable=self.status_text_var, fg_color='green',
                                                    hover_color='dark green', command=self.toggle)
        self.start_button.pack(side='left', padx=(0, 10))

        self.clear_button = customtkinter.CTkButton(self, text='Clear', command=lambda: self.output_panel.clear())
        self.clear_button.pack()

    def toggle(self):
        if self.status_var.get():
            self.stop()
        else:
            self.start()

    def start(self):
        self.status_text_var.set('Stop')
        self.status_var.set(True)
        self.start_button.configure(fg_color='red', hover_color='dark red')

        self.output_panel.insert('end', '[Monitoring]:')
        directories_to_monitor = self.directory_list_box.get_directories()
        for directory, data in directories_to_monitor.items():
            self.output_panel.insert('end', f'{directory:<100}')
            self.output_panel.insert('end', f'Recursive: {data["recursive"]}\n')
            self.pixel_monitor.monitor_folder(directory, data['recursive'])

        self.pixel_monitor.start()
        self.output_panel.insert('end', 'Started.')

    def stop(self):
        self.status_text_var.set('Start')
        self.status_var.set(False)
        self.start_button.configure(fg_color='green', hover_color='dark green')

        self.output_panel.insert('end', 'Stopped.')
        self.pixel_monitor.stop()

    def on_created(self, event):
        """Callback to handle new directories created."""
        if event.is_directory:
            self.output_panel.insert('end', f"New directory: {event.src_path}")
