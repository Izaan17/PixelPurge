from typing import Literal

import customtkinter

from widgets.buttons.state_button import StateButton


class ToggleIconButton(StateButton):
    def __init__(self,
                 master: any,
                 command: callable,
                 first_image: customtkinter.CTkImage,
                 second_image: customtkinter.CTkImage,
                 initial_state: Literal[0, 1] = 0,
                 **kwargs):

        # Initialize the StateButton part of the class
        initial_image = first_image if initial_state == 0 else second_image
        super().__init__(master, initial_state=initial_state, image=initial_image, **kwargs)

        # Set the images based on the state
        self.command = command
        self.first_image = first_image
        self.second_image = second_image

        # Configure the button click behavior
        self.configure(command=self.on_click)

    def on_click(self):
        """Handle button click."""
        # Execute the provided command
        self.command()

        # Toggle the state and update the image
        self.toggle_state()

        # Update the button's image after toggling
        self.update_image()

    def toggle_state(self):
        """Override the toggle function to update the state and image."""
        # Toggle the current state (using StateButton's toggle method)
        self.toggle()

    def update_image(self):
        """Update the button's image based on the current state."""
        if self.get_state() == 0:
            self.configure(image=self.first_image)
        else:
            self.configure(image=self.second_image)
