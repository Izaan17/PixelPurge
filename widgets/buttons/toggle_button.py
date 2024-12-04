from typing import Literal

from widgets.buttons.state_button import StateButton


class ToggleButton(StateButton):
    def __init__(
            self,
            parent,
            text_on="On",
            text_off="Off",
            colors_on=("lightgreen", "darkgreen"),  # Tuple for light/dark mode
            colors_off=("pink", "red"),  # Tuple for light/dark mode
            hover_colors_on=("darkolivegreen", "green"),  # Tuple for light/dark mode hover
            hover_colors_off=("lightcoral", "darkred"),  # Tuple for light/dark mode hover
            command_on=None,
            command_off=None,
            initial_state: Literal[0, 1] = 0,
            **kwargs
    ):
        # Initialize the StateButton
        super().__init__(parent, initial_state=initial_state, **kwargs)

        # Store attributes for the toggle states
        self.text_on = text_on
        self.text_off = text_off
        self.colors_on = colors_on
        self.colors_off = colors_off
        self.hover_colors_on = hover_colors_on
        self.hover_colors_off = hover_colors_off
        self.command_on = command_on
        self.command_off = command_off

        # Set the initial state
        self.update_button()

        # Bind the toggle functionality to the button
        self.configure(command=self.on_toggle)

    def update_button(self):
        """
        Updates the button's appearance based on the current state.
        """
        if self.get_state() == 1:  # "On" state
            self.configure(
                text=self.text_on,
                fg_color=self.colors_on,
                hover_color=self.hover_colors_on
            )
        else:  # "Off" state
            self.configure(
                text=self.text_off,
                fg_color=self.colors_off,
                hover_color=self.hover_colors_off
            )

    def on_toggle(self):
        """
        Toggles the state, updates the button, and executes the corresponding command.
        """
        self.toggle()  # Toggle the state
        self.update_button()  # Update the button's appearance

        # Execute the appropriate command based on the state
        if self.get_state() == 1 and self.command_on:
            self.command_on()
        elif self.get_state() == 0 and self.command_off:
            self.command_off()