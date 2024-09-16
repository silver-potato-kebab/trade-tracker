import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from edit_treeview import EditTreeview


class TradeTracker(tk.Tk):
    def __init__(self, name: str):
        super().__init__()

        self.title(name)
        self.main_frame = ttk.Frame(master=self)

        self.build_ui(master=self.main_frame)

        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def build_ui(self, master):

        column_names = {
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

        treeview = EditTreeview(master=master, columns=list(column_names.keys()))
        treeview.heading(column="#0", text="Date")
        treeview.column(column="#0", width=100)

        for col_name, col_text in column_names.items():
            treeview.heading(column=col_name, text=col_text)
            treeview.column(column=col_name, width=100)

        treeview.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":

    app = TradeTracker("My Trade Tracker App")

    app.mainloop()
