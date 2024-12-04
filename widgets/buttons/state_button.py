from typing import Literal
import customtkinter


class StateButton(customtkinter.CTkButton):
    def __init__(self, master: any, initial_state: Literal[0, 1] = 0, **kwargs):
        # Initialize the state (0 or 1)
        super().__init__(master, **kwargs)
        self.current_state = initial_state

    def toggle(self):
        """Toggle between state 0 and state 1."""
        self.set_state(1 - self.current_state)

    def set_state(self, state: int):
        """Set the state directly."""
        self.current_state = state

    def get_state(self) -> int:
        """Get the current state."""
        return self.current_state
