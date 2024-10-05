import tkinter as tk

from tkinter import ttk


class ValidatedEntry(ttk.Entry):
    """Validated Entry"""
    def __init__(self, master=None, validation_type: str=None, **kwargs):
        """
        Initialize Entry constructor with specified validation.

        Parameters:
        master: The Parent widget.
        validation_type:
            integer
            price
            alpha
        **kwargs: Additional keyword arguments passed to the ttk.Entry constructor.
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
        elif self.validation_type == "signed_price":
            return self.validate_signed_price(input)
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
        try:
            price = float(value)
            return price >= 0.0
        except ValueError:
            return False

    def validate_signed_price(self, value: str) -> bool:
        """Return True if value is a valid signed price."""
        if value in ("-", ".", "-.", ""): # Allow incomplete values during typing
            return True

        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_alpha(self, value: str) -> bool:
        """Return True if value is an alphabet character."""
        return value.isalpha()


if __name__ == "__main__":

    root = tk.Tk()

    v_entry = ValidatedEntry(validation_type="price")
    v_entry.pack()

    root.mainloop()
