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
        self.observer = None  # Initially, no observer

    def monitor_folder(self, folder, recursive=True):
        # If the observer is running, stop and reinitialize
        if self.observer and self.observer.is_alive():
            self.stop()  # Stop the current observer
        # Create a new observer and schedule the event handler
        self.observer = Observer()
        self.observer.schedule(self.event_handler, folder, recursive=recursive)

    def start(self):
        # Only start the observer if it's not already running
        if self.observer and not self.observer.is_alive():
            self.observer.start()

    def stop(self):
        # Stop the observer if it's running
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.unschedule_all()
            self.observer.join()  # Wait for the thread to terminate