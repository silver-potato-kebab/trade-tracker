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

        self.import_csv_file()

    def build_ui(self, master):
        """Create the graphical user interface on a master widget."""
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

    def export_csv_file(self):
        """Export to a CSV file."""
        file_exists = os.path.isfile("./test_tradetracker.csv")
        header = ("open_date","ticker", "long_short", "open_shares", "open_price", "net_cost", "close_date", "close_shares", "close_price", "net_proceeds")

        with open("test_tradetracker.csv", "a") as file:
            writer = csv.DictWriter(file, fieldnames=header)

            if not file_exists:
                writer.writeheader()

            pass

    def import_csv_file(self):
        """Import from a CSV file."""
        file_path = tk.filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])

        if file_path:
            try:
                with open(file_path, "r", newline="") as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        self.treeview.insert(parent="", index=tk.END, values=("1", "2"))

            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":

    app = TradeTracker("My Trade Tracker App")

    app.mainloop()
