from watchdog.events import FileSystemEventHandler, DirCreatedEvent, FileCreatedEvent
from watchdog.observers import Observer


class PixelWatcher(FileSystemEventHandler):
    def __init__(self):
        self.callbacks = []  # List of additional actions to trigger on file/directory creation

    def add_callback(self, callback):
        """Allow other components to register callbacks for on_created."""
        self.callbacks.append(callback)

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        # Trigger other registered actions
        for callback in self.callbacks:
            callback(event)


class PixelMonitor:
    def __init__(self, event_handler: FileSystemEventHandler):
        self.event_handler = event_handler
        self.observer = Observer()  # Single observer instance
        self.monitored_folders = set()  # Track monitored folders to prevent duplication

    def monitor_folder(self, folder, recursive=True):
        if folder not in self.monitored_folders:
            # Schedule the folder with the observer
            self.observer.schedule(self.event_handler, folder, recursive=recursive)
            self.monitored_folders.add(folder)

    def start(self):
        if not self.observer.is_alive():
            self.observer.start()

    def stop(self):
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()  # Wait for the observer thread to terminate
        self.monitored_folders.clear()  # Clear the tracked folders
