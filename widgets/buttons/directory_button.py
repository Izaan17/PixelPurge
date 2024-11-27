import customtkinter

class DirectoryButton(customtkinter.CTkButton):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=50, corner_radius=5, fg_color='#393e46', hover_color='#222831')
        self.configure(**kwargs)
