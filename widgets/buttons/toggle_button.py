from typing import Literal, Optional, Tuple, Callable, Union
import customtkinter

from widgets.buttons.state_button import StateButton


class ToggleButton(StateButton):
    def __init__(self,
                 master,
                 text_on: Optional[str] = None,
                 text_off: Optional[str] = None,
                 colors_on: Optional[Tuple[str, str]] = None,
                 colors_off: Optional[Tuple[str, str]] = None,
                 hover_colors_on: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_colors_off: Optional[Union[str, Tuple[str, str]]] = None,
                 first_image: Optional[customtkinter.CTkImage] = None,
                 second_image: Optional[customtkinter.CTkImage] = None,
                 command_on: Optional[Callable] = None,
                 command_off: Optional[Callable] = None,
                 command: Optional[Callable] = None,
                 initial_state: Literal[0, 1] = 0,
                 **kwargs):
        # Determine initial appearance based on the state
        initial_image = first_image if initial_state == 0 else second_image
        initial_text = text_off if initial_state == 0 else text_on

        super().__init__(master, initial_state=initial_state, image=initial_image, text=initial_text, **kwargs)

        # Store attributes
        self.text_on = text_on
        self.text_off = text_off
        self.colors_on = colors_on
        self.colors_off = colors_off
        self.hover_colors_on = hover_colors_on
        self.hover_colors_off = hover_colors_off
        self.first_image = first_image
        self.second_image = second_image
        self.command_on = command_on
        self.command_off = command_off
        self.command = command

        # Configure the button click behavior
        self.configure(command=self.on_click)

    def update_button(self):
        """
        Updates the button's appearance based on the current state.
        """
        state = self.get_state()
        if state == 1:
            # On state
            if self.text_on:
                self.configure(text=self.text_on)
            if self.colors_on:
                self.configure(fg_color=self.colors_on, hover_color=self.hover_colors_on)
            if self.second_image:
                self.configure(image=self.second_image)
        else:
            # Off state
            if self.text_off:
                self.configure(text=self.text_off)
            if self.colors_off:
                self.configure(fg_color=self.colors_off, hover_color=self.hover_colors_off)
            if self.first_image:
                self.configure(image=self.first_image)

    def on_click(self):
        """
        Handle button click: toggle state, update appearance, and execute commands.
        """
        self.toggle()  # Toggle the state
        self.update_button()  # Update the button's appearance

        # Execute the appropriate command
        if self.get_state() == 1:
            if self.command_on:
                self.command_on()
        else:
            if self.command_off:
                self.command_off()

        # Execute the common command, if any
        if self.command:
            self.command()