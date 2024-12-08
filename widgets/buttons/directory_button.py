import customtkinter


class DirectoryButton(customtkinter.CTkButton):
    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=35, width=50, corner_radius=5,
                       fg_color='#2563EB', hover_color='#1D4ED8', font=('', 14),
                       text_color='white')
        self.configure(**kwargs)
