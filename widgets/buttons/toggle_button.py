import customtkinter


class ToggleButton(customtkinter.CTkButton):
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
            initial_state=False,
            **kwargs
    ):

        # Determine initial colors and hover colors based on the state
        fg_color = colors_on if initial_state else colors_off
        hover_color = hover_colors_on if initial_state else hover_colors_off

        # Initialize the base class
        super().__init__(
            parent,
            text=text_on if initial_state else text_off,
            fg_color=fg_color,
            hover_color=hover_color,
            **kwargs
        )

        # Store attributes for the toggle states
        self.text_on = text_on
        self.text_off = text_off
        self.colors_on = colors_on
        self.colors_off = colors_off
        self.hover_colors_on = hover_colors_on
        self.hover_colors_off = hover_colors_off
        self.command_on = command_on
        self.command_off = command_off
        self.state = initial_state  # Current state of the button

        # Bind the toggle functionality to the button
        self.configure(command=self.toggle)

    def toggle(self):
        """
        Toggles the button's state and executes the corresponding command.
        """
        if self.state:
            # Transition to the "off" state
            self.configure(
                text=self.text_off,
                fg_color=self.colors_off,
                hover_color=self.hover_colors_off
            )
            if self.command_off:
                self.command_off()  # Call the off command if provided
        else:
            # Transition to the "on" state
            self.configure(
                text=self.text_on,
                fg_color=self.colors_on,
                hover_color=self.hover_colors_on
            )
            if self.command_on:
                self.command_on()  # Call the on command if provided

        # Toggle the state
        self.state = not self.state


if __name__ == '__main__':
    root = customtkinter.CTk()


    def start_action():
        print("Started!")


    def stop_action():
        print("Stopped!")


    toggle_button = ToggleButton(
        root,
        text_on="Start",
        text_off="Stop",
        colors_on=("lightgreen", "darkgreen"),  # Automatically handles light/dark mode
        colors_off=("pink", "red"),
        hover_colors_on=("darkolivegreen", "green"),
        hover_colors_off=("lightcoral", "darkred"),
        command_on=start_action,
        command_off=stop_action,
        initial_state=True
    )
    toggle_button.pack(pady=20)

    root.mainloop()
