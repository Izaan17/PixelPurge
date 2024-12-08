import customtkinter


class DefaultCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='#2563EB', hover_color='#1D4ED8')
        # Allow color overriding
        self.configure(**kwargs)
