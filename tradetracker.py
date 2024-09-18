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
        self.main_frame = ttk.Frame(master=self)

        self.build_ui(master=self.main_frame)

        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def build_ui(self, master):
        """Create the graphical user interface on a master widget."""
        buttons_frame = ttk.Frame(master=master)
        treeview_frame = ttk.Frame(master=master)
        status_frame = ttk.Frame(master=master)

        self.build_buttons(master=buttons_frame)
        self.build_treeview(master=treeview_frame)
        self.build_status_label(master=status_frame)

        buttons_frame.pack(anchor="w", pady=(0,20))
        treeview_frame.pack()
        status_frame.pack(pady=(20,0))

    def build_buttons(self, master):
        """Create buttons for the interface."""
        import_btn = ttk.Button(master=master, command=self.import_csv_file, text="Import")
        import_btn.pack(side=tk.LEFT)

        export_btn = ttk.Button(master=master, command=self.export_csv_file, text="Export")
        export_btn.pack(padx=(10, 0), side=tk.LEFT)

    def build_treeview(self, master):
        """Create the custom treeview widget."""
        column_names = {
            "open_date": "Date",
            "ticker": "Ticker",
            "long_short": "Long/Short",
            "open_shares": "Shares",
            "open_price": "Price",
            "net_cost": "Net Cost",
            "total_cost": "Total Cost",
            "cost_basis": "Cost Basis",
            "close_date": "Exit Date",
            "close_shares": "Shares",
            "close_price": "Price",
            "net_proceeds": "Net Proceeds",
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

    def write_csv_file(self, path):
        """Write treeview data  to CSV file."""
        header = ("open_date","ticker", "long_short", "open_shares", "open_price", "net_cost", "close_date", "close_shares", "close_price", "net_proceeds")

        with open(path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            iids = reversed(self.treeview.get_children())
            for iid in iids:
                row = self.treeview.set(iid)
                if row:
                    # need to fix this dictionary. Contain columns not in header
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
        iids = self.treeview.get_children()

        upper_row_iid = None

        open_date_temp = ""
        ticker_temp = ""
        long_short_temp = ""

        total_cost = None
        total_shares = None
        total_net_proceeds = None

        for iid in iids:
            row = self.treeview.set(iid)

            # If row is not empty
            if row:
                open_date = row["open_date"]
                ticker = row["ticker"]
                long_short = row["long_short"]
                open_shares = row["open_shares"]
                net_cost = row["net_cost"]
                net_proceeds = row["net_proceeds"]

                # If same trade
                if (open_date_temp == open_date) and (ticker_temp == ticker) and (long_short_temp == long_short):
                    total_cost += float(net_cost)
                    total_shares += float(open_shares)
                    if net_proceeds:
                        total_net_proceeds += float(net_proceeds)
                # Else if new trade
                else:
                    # Perform calculations for previous trade excluding the very first trade.
                    if (total_cost != None) and (total_shares != None) and (total_net_proceeds != None):
                        total_cost = round(total_cost, 2)
                        cost_basis = round(total_cost/total_shares, 2)
                        profit_loss = round(total_net_proceeds - total_cost, 2)

                        self.treeview.set(item=upper_row_iid, column="total_cost", value=total_cost)
                        self.treeview.set(item=upper_row_iid, column="cost_basis", value=cost_basis)
                        self.treeview.set(item=upper_row_iid, column="profit_loss", value=profit_loss)

                    # Update temp variables for the new trade.
                    upper_row_iid = iid

                    open_date_temp = open_date
                    ticker_temp = ticker
                    long_short_temp = long_short

                    total_cost = float(net_cost)
                    total_shares = float(open_shares)
                    if net_proceeds:
                        total_net_proceeds = float(net_proceeds)

            else:
                total_cost = round(total_cost, 2)
                cost_basis = round(total_cost/total_shares, 2)
                profit_loss = round(total_net_proceeds - total_cost, 2)

                self.treeview.set(item=upper_row_iid, column="total_cost", value=total_cost)
                self.treeview.set(item=upper_row_iid, column="cost_basis", value=cost_basis)
                self.treeview.set(item=upper_row_iid, column="profit_loss", value=profit_loss)


if __name__ == "__main__":

    app = TradeTracker("My Trade Tracker App")

    app.mainloop()
