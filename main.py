import shutil
import time
import tkinter as tk
from tkinter import font
from tkinter import messagebox

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Watcher(FileSystemEventHandler):
    def __init__(self):
        self.new_directories = []  # List to store created directories

    def on_created(self, event):
        if event.is_directory:  # Only track directories
            self.new_directories.append(event.src_path)
            print(event.src_path)

    def get_new_directories(self):
        return self.new_directories

def monitor_folders(folders_to_monitor, watcher):
    event_handler = watcher
    observer = Observer()

    # Schedule the observer for each folder in the list
    for folder in folders_to_monitor:
        observer.schedule(event_handler, folder, recursive=True)
        print(f"Monitoring folder: {folder}")

    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")
    observer.join()

def show_gui(folders_to_delete):
    # Create the root window for the GUI
    root = tk.Tk()
    root.title("Newly Created Folders")

    # Set window size and padding for a nicer look
    root.geometry("600x400")
    root.resizable(False, False)

    # Set a nice font for the labels and buttons
    custom_font = font.Font(family="Helvetica", size=12)

    # Title label
    title_label = tk.Label(root, text="New Directories Detected", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Display the list of folders
    label = tk.Label(root, text="Select folders to delete:", font=custom_font)
    label.pack(pady=5)

    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, font=custom_font)
    for folder in folders_to_delete:
        listbox.insert(tk.END, folder)
    listbox.pack(pady=10, padx=20, fill=tk.BOTH)

    # Automatically select all folders by default
    for i in range(len(folders_to_delete)):
        listbox.select_set(i)

    def delete_selected():
        selected_folders = [listbox.get(i) for i in listbox.curselection()]
        if selected_folders:
            for folder in selected_folders:
                try:
                    shutil.rmtree(folder)  # Delete the directory
                    print(f"Deleted folder: {folder}")
                except OSError as e:
                    print(f"Failed to delete {folder}: {e}")
            messagebox.showinfo("Deleted", "Selected folders have been deleted.")
        else:
            messagebox.showwarning("No Selection", "No folders selected for deletion.")
        root.quit()

    def cancel():
        root.quit()

    # Buttons for user actions
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    delete_button = tk.Button(button_frame, text="Delete Selected Folders", command=delete_selected, font=custom_font, bg="#ff6347", fg="white", width=20)
    delete_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel, font=custom_font, bg="#4CAF50", fg="white", width=20)
    cancel_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    # List of folders to monitor
    folders_to_monitor = [
        r"C:\Users\izaan\AppData\Local",  # Change this to your actual folder paths
        r"C:\Users\izaan\AppData\LocalLow",  # Another folder to monitor
        r"C:\Users\izaan\AppData\Roaming"   # Add as many folders as needed
    ]

    watcher = Watcher()
    monitor_folders(folders_to_monitor, watcher)

    # After monitoring ends, show the GUI with the new directories
    new_directories = watcher.get_new_directories()
    show_gui(new_directories)
