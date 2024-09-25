import tkinter as tk

from tkinter import ttk


class ValidatedEntry(ttk.Entry):
    """Validated Entry"""
    def __init__(self, master=None, validation_type: str=None, **kwargs):
        """
        Initialize Entry constructor with specified validation.

        validation_type (str):
        integer
        price
        alpha
        """
        super().__init__(master, **kwargs)

        self.validation_type = validation_type
        self.validate_func = self.register(self.validate_entry)

        self.config(validate="key", validatecommand=(self.validate_func, "%P"))

    def validate_entry(self, input) -> bool:
        """Validate user input."""
        if input == "":
            return True

        if self.validation_type == "integer":
            return self.validate_integer(input)

        elif self.validation_type == "price":
            return self.validate_price(input)

        elif self.validation_type == "alpha":
            return self.validate_alpha(input)

        else:
            self.delete(0, tk.END)
            self.insert(0, "Invalid validation_type")
            return False

    def validate_integer(self, value: str) -> bool:
        """Return True if value is an integer."""
        return value.isdigit()

    def validate_price(self, value: str) -> bool:
        """Return True if value is valid price."""
        return value.is

    def validate_alpha(self, value: str) -> bool:
        """Return True if value is an alphabet character."""
        pass


if __name__ == "__main__":

    root = tk.Tk()

    v_entry = ValidatedEntry(validation_type="integer")
    v_entry.pack()

    root.mainloop()
