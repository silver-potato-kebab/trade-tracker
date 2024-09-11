import tkinter as tk
import csv


class MainApp(tk.Tk):
    def __init__(self, name: str, dimension: tuple[int, int]):
        super().__init__()

        self.title(name)
        self.geometry(f"{dimension[0]}x{dimension[1]}")

        self.column_labels = ["Date", "Long/Short", "Shares", "Price", "Net Cost", "Total Cost", "Cost Basis"]

        self.create_columns()

        self.status_label = tk.Label(self, text="Status: Placeholder Label", padx=20, pady=10)
        self.status_label.grid(stick="nsew")

    def create_columns(self):
        for col, label in enumerate(self.column_labels):
            label = tk.Label(self, text=label, borderwidth=1, relief="solid", padx=10, pady=10)
            label.grid(row=0, column=col, stick="nsew")


    def open_csv_file(self):
        file_path = tk.filedialog.askopenfilename(tile="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            display_csv_data(file_path)

    def display_csv_data(self, file_path):
        try:
            pass
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")


if __name__ == "__main__":
    app = MainApp("Trade Tracker", (960, 540))
    app.mainloop()
