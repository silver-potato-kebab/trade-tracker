import csv
import tkinter as tk
from tkinter import filedialog


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

        # Middle Container (Trade log)
        self.mid_frame = tk.Frame(self)
        self.mid_frame.pack(padx=10, pady=(5, 5))

        self.column_labels = ["Date", "Long/Short", "Shares", "Price", "Net Cost", "Total Cost", "Cost Basis"]
        self.create_columns()

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
            self.status_label.config(text=f"CSV file loaded: {file_path}")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")


if __name__ == "__main__":
    app = MainApp("Trade Tracker")
    app.mainloop()
