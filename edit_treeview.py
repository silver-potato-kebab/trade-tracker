import tkinter as tk
from tkinter import ttk
from typing import Callable
from validated_entry import ValidatedEntry


class EditTreeview(ttk.Treeview):
    """Editable ttk Treeview widget that displays a hierarchical collection of items."""

    def __init__(self, master, column_validation: dict[str, str]=None, callback: Callable[[], None]=None, **kw):
        """Initialize the EditTreeview with the parent master and optional keyword arguments.

        Parameters:
        master: The parent widget.
        column_validation: {column_name: validation_type (integer, price, alpha)}
        **kw: Additional keyword arguments passed to the ttk.Treeview constructor.
        """
        super().__init__(master, **kw)

        self.column_validation = column_validation
        self.callback = callback

        self.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        """Instantiate Entry widget on top of a Treeview cell for editing."""

        region_clicked = self.identify_region(x=event.x, y=event.y)

        # Only enable double clicking in "tree" or "cell", not "heading" or "nothing".
        if region_clicked not in ("tree", "cell"):
            return

        # Get column that was double clicked: #0, #1, #2, etc.
        column = self.identify_column(x=event.x)
        column_index = int(column[1:]) - 1 # "#0" -> -1, "#1" -> 0, "#2" -> 1, etc.

        # Get iid of the item selected (row identifier). For example: "I001", "I002", etc.
        selected_iid = self.focus()

        # Get dictionary containing both text (for a tree) and value (for a cell) from the given item iid.
        selected_values = self.item(selected_iid)

        if column == "#0": # if tree is selected
            selected_text = selected_values.get("text")
        else: # else cell is selected
            values = selected_values.get("values")

            # Check if the column index is within the valid range of available columns
            if column_index >= len(values):
                return # Column index out of range, do nothing

            selected_text = values[column_index]

        # Get the coordinate and dimension of tree or cell -> (x, y, w, h)
        column_box = self.bbox(item=selected_iid, column=column)

        if self.column_validation:
            column_name = self.column(column)["id"]
            validation_type = self.column_validation.get(column_name, None)
            entry_edit=ValidatedEntry(validation_type=validation_type) if validation_type else ttk.Entry()

            # Keep track of validation type for event reference
            entry_edit.validation_type = validation_type
        else:
            entry_edit = ttk.Entry()

        # Keep track of column_index and selected_iid inside the ttk.Entry object for event reference.
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        entry_edit.insert(0, selected_text) # insert text from tree/cell into Entry widget
        entry_edit.selection_range(0, tk.END) # select all text inside Entry widget
        entry_edit.focus() # place cursor inside Entry widget

        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        # Offset any padding by factoring in the difference between the widget's and toplevel's (x, y) coordinates.
        tree_x_offset = self.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
        tree_y_offset = self.winfo_rooty() - self.winfo_toplevel().winfo_rooty()

        entry_edit.place(x=column_box[0]+tree_x_offset,
                         y=column_box[1]+tree_y_offset,
                         w=column_box[2],
                         h=column_box[3])

    def on_focus_out(self, event):
        """Remove Entry widget when not in focus."""

        event.widget.destroy()

    def on_enter_pressed(self, event):
        """Update text in cell when pressing enter."""

        new_text = event.widget.get().strip()

        # Get item ID being edited, such as I002.
        selected_iid = event.widget.editing_item_iid

        # Handle validation and formatting based on column validation
        if self.column_validation:
            try:
                validation_type = event.widget.validation_type
                if validation_type in ("price", "signed_price"):
                    new_text = self.format_price(new_text)
            except AttributeError:
                pass # No validation type, do nothing

        column_index = event.widget.editing_column_index # Get the column index

        # Update the Treeview item based on whether it's a tree column or a regular column
        if column_index == -1: # If it's the tree column
            self.item(selected_iid, text=new_text)
        else: # If it's a regular column
            current_values = self.item(selected_iid).get("values")
            current_values[column_index] = new_text
            self.item(selected_iid, values=current_values)

        event.widget.destroy()

        self.callback() if self.callback else None

    def format_price(self, value: str) -> str:
        """Helper function to format price or signed price fields."""
        try:
            # Convert to float and ensure formatting to 2 decimal places
            return f"{float(value) + 0:.2f}"
        except ValueError:
            return "0.00"  # Default to 0.00 on invalid input


if __name__ == "__main__":

    root = tk.Tk()

    column_names = ("column_#1", "column_#2", "column_#3")
    treeview = EditTreeview(root, columns=column_names)

    treeview.heading(column="#0", text="Column 0") # "#0" is tkinter's reference to the very first column
    treeview.heading(column="column_#1", text="Column 1")
    treeview.heading(column="column_#2", text="Column 2")
    treeview.heading(column="column_#3", text="Column 3")

    tree_1 = treeview.insert(parent="",
                             index=tk.END,
                             text="tree_1")

    treeview.insert(parent=tree_1,
                             index=tk.END,
                             values=("Cell Col 1", "Cell Col 2", "Cell Col 3"))

    treeview.insert(parent=tree_1,
                             index=tk.END,
                             values=("Cell Col 1", "Cell Col 2", "Cell Col 3"))

    tree_2 = treeview.insert(parent="",
                             index=tk.END,
                             text="tree_2")

    treeview.insert(parent=tree_2,
                             index=tk.END,
                             values=("Cell Col 1", "Cell Col 2", "Cell Col 3"))

    treeview.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
