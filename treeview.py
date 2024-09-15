import tkinter as tk
from tkinter import ttk


class TreeviewEdit(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.bind("<Double-1>", self.on_double_click) # double left click

    def on_double_click(self, event):

        # Identify the region that was double clicked.
        region_clicked = self.identify_region(x=event.x, y=event.y)

        # We're only interested in tree and cell.
        if region_clicked not in ("tree", "cell"):
            return

        # Which item was double-clicked?
        # For example, "#0" is the first column, followed by "#1", "#2", etc.
        column = self.identify_column(x=event.x)

        # For example, "#0" will become -1, "#1" will become 0, etc..
        column_index = int(column[1:]) - 1

        # For example: I001
        selected_iid = self.focus()

        # This will contain both text and values from the given item iid.
        selected_values = self.item(selected_iid)

        if column == "#0":
            selected_text = selected_values.get("text")
        else:
            selected_text = selected_values.get("values")[column_index]

        column_box = self.bbox(item=selected_iid, column=column) # returns (x, y, w, h)

        entry_edit = tk.Entry(root)

        # Record the column index and item iid.
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        entry_edit.insert(0, selected_text)
        entry_edit.selection_range(0, tk.END)

        entry_edit.focus()

        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        entry_edit.place(x=column_box[0],
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3])

    def on_focus_out(self, event):
        event.widget.destroy()

    def on_enter_pressed(self, event):
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

    column_names = ("vehicle_name", "year", "color")

    treeview_vehicles = TreeviewEdit(root, columns=column_names)

    treeview_vehicles.heading("#0", text="Vehicle Type") # "#0" is tkinter's reference to the very first column
    treeview_vehicles.heading("vehicle_name", text="Vehicle Name")
    treeview_vehicles.heading("year", text="Year")
    treeview_vehicles.heading("color", text="Color")

    sedan_row = treeview_vehicles.insert(parent="",
                             index=tk.END,
                             text="Sedan")

    treeview_vehicles.insert(parent=sedan_row,
                             index=tk.END,
                             values=("Nissan Versa", "2010", "Silver"))

    treeview_vehicles.insert(parent=sedan_row,
                             index=tk.END,
                             values=("Toyota Camry", "2012", "Blue"))

    treeview_vehicles.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
