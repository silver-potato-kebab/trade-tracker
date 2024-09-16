import tkinter as tk
from tkinter import ttk


class EditTreeview(ttk.Treeview):
    """Editable ttk Treeview widget that displays a hierarchical collection of items."""

    def __init__(self, master, **kw):
        """Initialize the EditTreeview with the parent master and optional keyword arguments.

        Parameters:
        master: The parent widget.
        **kw: Additional keyword arguments passed to the ttk.Treeview constructor.
        """
        super().__init__(master, **kw)

        self.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        """Instantiate Entry widget on top of a Treeview cell for editing."""

        region_clicked = self.identify_region(x=event.x, y=event.y)

        # Only enable double clicking in "tree" or "cell", not "heading" or "nothing".
        if region_clicked not in ("tree", "cell"):
            return

        # Get column that was double clicked: #0, #1, #2, etc.
        column = self.identify_column(x=event.x)

        # "#0" -> -1, "#1" -> 0, "#2" -> 1, etc.
        column_index = int(column[1:]) - 1

        # Get iid of the item selected (row identifier). For example: "I001", "I002", etc.
        selected_iid = self.focus()

        # Get dictionary containing both text (for a tree) and value (for a cell) from the given item iid.
        selected_values = self.item(selected_iid)

        if column == "#0": # if tree
            selected_text = selected_values.get("text")
        else: # else cell
            selected_text = selected_values.get("values")[column_index]

        # Get the coordinate and dimension of tree or cell -> (x, y, w, h)
        column_box = self.bbox(item=selected_iid, column=column)

        entry_edit = ttk.Entry(root)

        # Keep track of column_index and selected_iid inside the ttk.Entry object for event reference.
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        entry_edit.insert(0, selected_text) # insert text from tree/cell into Entry widget
        entry_edit.selection_range(0, tk.END) # select all text inside Entry widget
        entry_edit.focus() # place cursor inside Entry widget

        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        entry_edit.place(x=column_box[0],
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3])

    def on_focus_out(self, event):
        """Remove Entry widget when not in focus."""

        event.widget.destroy()

    def on_enter_pressed(self, event):
        """Update text in cell when pressing enter."""

        new_text = event.widget.get()

        # Such as I002
        selected_iid = event.widget.editing_item_iid

        # Such as -1 (tree column), 0 (first self-defined column), etc.
        column_index = event.widget.editing_column_index

        if column_index == -1:
            self.item(selected_iid, text=new_text)
        else:
            current_values = self.item(selected_iid).get("values")
            current_values[column_index] = new_text
            self.item(selected_iid, values=current_values)

        event.widget.destroy()


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
