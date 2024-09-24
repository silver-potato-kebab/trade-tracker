import traceback

import csv
import os.path
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from edit_treeview import EditTreeview


class TradeTracker(tk.Tk):
    """Application for tracking trades. Can import and export transactions in a CSV file."""
    def __init__(self, name: str):
        """Constructor for TradeTracker. Instsantiate various widgets for the user interface."""
        super().__init__()

        self.title(name)
        self.main_frame = ttk.Frame(master=self, name="main_frame")

        self.build_ui(master=self.main_frame)

        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def build_ui(self, master):
        """Create the graphical user interface on a master widget."""
        buttons_frame = ttk.Frame(master=master)
        order_entry_frame = ttk.LabelFrame(master=master, name="order_entry_frame", text="Order Entry")
        treeview_frame = ttk.Frame(master=master)
        status_frame = ttk.Frame(master=master)

        self.build_buttons(master=buttons_frame)
        self.build_order_entry(master=order_entry_frame)
        self.build_treeview(master=treeview_frame)
        self.build_status_label(master=status_frame)

        buttons_frame.pack(anchor="w", pady=(0,20))
        order_entry_frame.pack(anchor="w", pady=(0,20))
        treeview_frame.pack(pady=(0,20))
        status_frame.pack()

    def build_buttons(self, master):
        """Create buttons for the interface."""
        import_btn = ttk.Button(master=master, command=self.import_csv_file, text="Import")
        import_btn.pack(side=tk.LEFT)

        export_btn = ttk.Button(master=master, command=self.export_csv_file, text="Export")
        export_btn.pack(padx=(10, 0), side=tk.LEFT)

    def build_order_entry(self, master):
        """Create order entry form."""

        def update_cost_entry(var, index, mode):
            """Update Cost entry widget."""
            cost_entry_widget = self.nametowidget(".main_frame.order_entry_frame.entry_inner_frame.cost")
            cost = shares_intvar.get() * price_doublevar.get()
            cost_entry_widget.config(state="normal")
            cost_entry_widget.delete(0, tk.END)
            cost_entry_widget.insert(0, cost)
            cost_entry_widget.config(state="readonly")

        entry_inner_frame = ttk.Frame(master=master, name="entry_inner_frame")

        entry_labels = ("Date", "Ticker", "Long/Short", "Shares", "Price", "Cost")

        special_cases = {
            "Date": lambda frame, col, label_text: DateEntry(master=frame, name=label_text, width=12).grid(row=1, column=col, padx=1),
            "Long/Short": lambda frame, col, label_text: ttk.Combobox(frame, values=["Long", "Short"], name=label_text, width=12).grid(row=1, column=col, padx=1),
            "Cost": lambda frame, col, label_text: ttk.Entry(master=frame, name=label_text, width=12, state="readonly").grid(row=1, column=col, padx=1)
        }

        for col, label_text in enumerate(entry_labels):
            # Create the label
            label =  ttk.Label(master=entry_inner_frame, text=label_text)
            label.grid(row=0, column=col, pady=(0,10))

            # Create entry or special widget
            if label_text in special_cases:
                special_cases[label_text](entry_inner_frame, col, self.lowercase_ignore_special(label_text))
            elif label_text == "Shares":
                shares_intvar  = tk.IntVar()
                shares_intvar.trace_add("write", update_cost_entry)
                ttk.Entry(master=entry_inner_frame, textvariable=shares_intvar, name=self.lowercase_ignore_special(label_text), width=12).grid(row=1, column=col, padx=1)
            elif label_text == "Price":
                price_doublevar = tk.DoubleVar()
                price_doublevar.trace_add("write", update_cost_entry)
                ttk.Entry(master=entry_inner_frame, textvariable=price_doublevar, name=self.lowercase_ignore_special(label_text), width=12).grid(row=1, column=col, padx=1)
            else:
                ttk.Entry(master=entry_inner_frame, name=self.lowercase_ignore_special(label_text), width=12).grid(row=1, column=col, padx=1)

        entry_inner_frame.pack(padx=10, pady=10, side=tk.LEFT)

        # 'Add' button
        button = ttk.Button(master=entry_inner_frame, text="Add", command=self.add_entry)
        button.grid(row=1, column=99, padx=(10,0))

    def build_treeview(self, master):
        """Create the custom treeview widget."""
        column_names = {
            "open_date": "Date",
            "ticker": "Ticker",
            "long_short": "Long/Short",
            "open_shares": "Shares",
            "open_price": "Price",
            "cost": "Cost",
            "total_cost": "Total Cost",
            "cost_basis": "Cost Basis",
            "close_date": "Exit Date",
            "close_shares": "Shares",
            "close_price": "Price",
            "proceeds": "Proceeds",
            "profit_loss": "Profit/Loss",
            "net_percentage": "Net %"}

        self.treeview = EditTreeview(master=master, columns=list(column_names.keys()), show="headings")

        for col_name, col_text in column_names.items():
            self.treeview.heading(column=col_name, text=col_text)
            self.treeview.column(column=col_name, width=100)

        self.treeview.pack(fill=tk.BOTH, expand=True)

    def build_status_label(self, master):
        """Create a status label for the interface."""
        self.status_label = ttk.Label(master=master, text="")
        self.status_label.pack()

    def lowercase_ignore_special(self, text):
        """Find all alphabetic characters and convert only them to lowercase"""
        return ''.join(char.lower() if char.isalpha() else char for char in text)

    def write_csv_file(self, path):
        """Write treeview data  to CSV file."""
        header = ("open_date","ticker", "long_short", "open_shares", "open_price", "cost", "close_date", "close_shares", "close_price", "proceeds")

        with open(path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            iids = reversed(self.treeview.get_children())
            for iid in iids:
                row = self.treeview.set(iid)
                if row:
                    data = {k: v for k, v in row.items() if k in header}
                    writer.writerow(data)

    def autosave(self):
        """Autosave data to a CSV file."""
        pass
        

    def export_csv_file(self):
        """Export to a CSV file."""
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])

        if file_path:
            self.write_csv_file(file_path)

    def add_entry(self):
        """Add entry values to treeview and export to current CSV file."""
        entry_inner_frame = self.nametowidget(".main_frame.order_entry_frame.entry_inner_frame")

        data = {
            "open_date": entry_inner_frame.nametowidget("!dateentry").get_date(),
            "ticker": entry_inner_frame.nametowidget("ticker").get(),
            "long_short": entry_inner_frame.nametowidget("long/short").get(),
            "open_shares": entry_inner_frame.nametowidget("shares").get(),
            "open_price": entry_inner_frame.nametowidget("price").get(),
            "cost": entry_inner_frame.nametowidget("cost").get()
        }

        new_item = self.treeview.insert(parent="", index=0)
        columns = ("open_date", "ticker", "long_short", "open_shares", "open_price", "cost")

        for col, val in data.items():
            self.treeview.set(item=new_item, column=col, value=val)

    def import_csv_file(self):
        """Import from a CSV file."""
        file_path = tk.filedialog.askopenfilename(title="Import CSV File", filetypes=[("CSV Files", "*.csv")])

        if file_path:
            self.treeview.delete(*self.treeview.get_children()) # Clear current data
            try:
                with open(file_path, "r", newline="") as file:
                    csv_reader = csv.DictReader(file)
                    temp_date = ""
                    for row in csv_reader:
                        new_item = self.treeview.insert(parent="", index=0)
                        # Add empty row to separate different dates
                        if row["open_date"] != temp_date:
                            new_item = self.treeview.insert(parent="", index=0)
                            temp_date = row["open_date"]

                        for col_name, value in row.items():
                            self.treeview.set(item=new_item, column=col_name, value=value)

                self.perform_all_calculations()
                self.status_label.config(text=f"CSV file loaded: {file_path}")

            except Exception as e:
                self.status_label.config(text=f"Error: {e}")
                print(traceback.format_exc())


    def perform_all_calculations(self):
        """Perform all calculations for Treeview."""

        def calculate_and_set_values(iid, total_cost, total_shares, total_net_proceeds):
            """Helper method to calculate and set total cost, cost basis, and profit/loss."""
            total_cost = round(total_cost, 2)
            cost_basis = round(total_cost / total_shares, 2)
            profit_loss = round(total_net_proceeds - total_cost, 2)
            net_percentage = round(profit_loss/total_cost*100, 2)

            self.treeview.set(item=iid, column="total_cost", value=total_cost)
            self.treeview.set(item=iid, column="cost_basis", value=cost_basis)
            self.treeview.set(item=iid, column="profit_loss", value=profit_loss)
            self.treeview.set(item=iid, column="net_percentage", value=net_percentage)

        iids = self.treeview.get_children()

        # Temporary variables to track ongoing trade
        upper_row_iid = None
        open_date_temp = ticker_temp = long_short_temp = ""
        total_cost = total_shares = total_net_proceeds = None

        for iid in iids:
            row = self.treeview.set(iid)

            # If the row is not empty
            if row:
                open_date, ticker, long_short = row["open_date"], row["ticker"], row["long_short"]
                open_shares, net_cost = float(row["open_shares"]), float(row["cost"])
                net_proceeds = float(row["proceeds"]) if row["proceeds"] else 0

                # If continuing the same trade (multiple entries/transactions)
                if (open_date_temp == open_date) and (ticker_temp == ticker) and (long_short_temp == long_short):
                    total_cost += net_cost
                    total_shares += open_shares
                    total_net_proceeds += net_proceeds

                # For a new trade
                else:
                    # Calculate the previous trade's values if any (all trades except the very first one)
                    if total_cost is not None:
                        calculate_and_set_values(upper_row_iid, total_cost, total_shares, total_net_proceeds)

                    # Update temp variables for the new trade
                    upper_row_iid = iid
                    open_date_temp, ticker_temp, long_short_temp = open_date, ticker, long_short
                    total_cost, total_shares, total_net_proceeds = net_cost, open_shares, net_proceeds

            # Empty row encountered; process the previous trade's calculations.
            else:
                calculate_and_set_values(upper_row_iid, total_cost, total_shares, total_net_proceeds)


if __name__ == "__main__":

    app = TradeTracker("My Trade Tracker App")

    app.mainloop()
