import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry


class MainApp(tk.Tk):
    def __init__(self, name: str):
        super().__init__()

        self.title(name)

        # Top Container (Button, Ticker)
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(padx=10, pady=(10, 5), anchor="w")

        self.open_csv_btn = tk.Button(self.top_frame, text="Open CSV", command=self.open_csv_file)
        self.open_csv_btn.pack(side=tk.LEFT)
        self.ticker_label = tk.Label(self.top_frame, text="Ticker:")
        self.ticker_label.pack(side=tk.LEFT, padx=(10, 5))
        self.ticker_entry = tk.Entry(self.top_frame, width=8)
        self.ticker_entry.pack(side=tk.LEFT)

        # Input Section
        self.input_frame = tk.LabelFrame(self, text="Input")
        self.input_frame.pack(padx=10, pady=5)

        self.input_labels = ["Ticker", "Date", "Long/Short", "Shares", "Price", "Net Cost", "Total Cost", "Cost Basis"]
        for col, label in enumerate(self.input_labels):
            label = tk.Label(self.input_frame, text=label, padx=20, pady=10)
            label.grid(row=0, column=col)

        self.ticker_entry1 = tk.Entry(self.input_frame, width=10)
        self.ticker_entry1.grid(row=1, column=0)

        self.date_entry1 = DateEntry(self.input_frame, width=10)
        self.date_entry1.grid(row=1, column=1)

        self.pos_type1 = ttk.Combobox(self.input_frame, values=["Long", "Short"], width=10)
        self.pos_type1.grid(row=1, column=2)

        self.shares_entry1 = tk.Entry(self.input_frame, width=10)
        self.shares_entry1.grid(row=1, column=3)

        self.price_entry1 = tk.Entry(self.input_frame, width=10)
        self.price_entry1.grid(row=1, column=4)

        self.netcost_entry1 = tk.Entry(self.input_frame, width=10)
        self.netcost_entry1.grid(row=1, column=5)


        # Middle Container (Trade log)
        self.mid_frame = tk.Frame(self)
        self.mid_frame.pack(padx=10, pady=5)

        self.column_labels = ["Date", "Long/Short", "Shares", "Price", "Net Cost", "Total Cost", "Cost Basis"]
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Bottom Container (Status label)
        self.bot_frame = tk.Frame(self)
        self.bot_frame.pack(padx=10, pady=(5, 10))

        self.status_label = tk.Label(self.bot_frame, text="Status: Placeholder Label")
        self.status_label.pack()


    def create_columns(self):
        for col, label in enumerate(self.column_labels):
            label = tk.Label(self.mid_frame, text=label, borderwidth=1, relief="solid", padx=10, pady=10)
            label.grid(row=0, column=col, stick="nsew")

    def open_csv_file(self):
        file_path = tk.filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.display_csv_data(file_path)

    def display_csv_data(self, file_path):
        try:
            with open(file_path, "r", newline="") as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)
                print(header)
                self.tree.delete(*self.tree.get_children()) # Clear current data

                self.tree["columns"] = header
                for col in header:
                    print(col)
                    self.tree.heading(col, text=col)
                    self.tree.column(col, stretch=tk.NO, width=100)

                for row in csv_reader:
                    self.tree.insert("", tk.END, values=row)

                self.tree["show"] = "headings"
                self.status_label.config(text=f"CSV file loaded: {file_path}")

        except Exception as e:
            self.status_label.config(text=f"Error: {e}")


if __name__ == "__main__":
    app = MainApp("Trade Tracker")
    app.mainloop()
