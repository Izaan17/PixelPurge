import customtkinter


class ToggleIconButton(customtkinter.CTkButton):
    def __init__(self,
                 master: any,
                 command: callable,
                 first_image: customtkinter.CTkImage,
                 second_image: customtkinter.CTkImage,
                 initial_state: int = 0,  # Added initial_state parameter
                 **kwargs):

        # Check the initial_state and set the initial image accordingly
        initial_image = first_image
        if initial_state:
            initial_image = second_image

        super().__init__(master, image=initial_image, **kwargs)

        self.command = command
        self.first_image = first_image
        self.second_image = second_image
        self.current_image = initial_image  # Set the current image to the initial image

        self.configure(command=self.on_click)

    def on_click(self):
        # Run the command
        self.command()

        # Toggle the image
        self.current_image = self.second_image if self.current_image == self.first_image else self.first_image

        # Update the button's image
        self.configure(image=self.current_image)
