from typing import Literal
import customtkinter

class ToggleIconButton(customtkinter.CTkButton):
    def __init__(self,
                 master: any,
                 command: callable,
                 first_image: customtkinter.CTkImage,
                 second_image: customtkinter.CTkImage,
                 initial_state: Literal[0, 1] = 0,
                 **kwargs):

        # Set initial image based on initial_state
        initial_image = first_image if initial_state == 0 else second_image
        super().__init__(master, image=initial_image, **kwargs)

        self.command = command
        self.current_state = initial_state
        self.first_image = first_image
        self.second_image = second_image
        self.current_image = initial_image

        self.configure(command=self.on_click)

    def on_click(self):
        # Run the command when the button is clicked
        self.command()

        # Toggle the state and image
        self.toggle_state()

        # Update the button's image after toggling
        self.configure(image=self.current_image)

    def toggle_state(self):
        """Toggle between first and second image."""
        # Toggle the current state
        self.set_state(1 - self.current_state)

    def set_state(self, state: int):
        """Set the state and image directly."""
        if state == 0:
            self.current_image = self.first_image
        else:
            self.current_image = self.second_image
        self.current_state = state
        self.configure(image=self.current_image)
