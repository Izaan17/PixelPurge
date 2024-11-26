import customtkinter
from functools import wraps

class OutputPanel(customtkinter.CTkTextbox):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(state='disabled')

    @staticmethod
    def enable_editing(func):
        """
        Decorator that temporarily enables editing for a method call.
        Automatically disables editing after the method completes.
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.configure(state='normal')
            try:
                result = func(self, *args, **kwargs)
                return result
            finally:
                self.configure(state='disabled')
        return wrapper

    @enable_editing
    def insert(self, index: str, text: str, end: str = '\n', tags=None):
        """Insert text at specified index with optional end string and tags."""
        super().insert(index, text + end, tags)

    @enable_editing
    def clear(self):
        """Clear all text from the textbox."""
        self.delete("1.0", "end")