import csv
import os.path


file_exists = os.path.isfile("./sample.csv")
header = ["id", "date", "ticker", "price", "shares", "total"]


with open("sample.csv", "a") as f:
    writer = csv.DictWriter(f, fieldnames=header)

    if not file_exists:
        writer.writeheader()

    writer.writerow({"id": 1, "date": "2024-09-14", "ticker": "TQQQ", "price": 9.45, "shares": 100, "total": 945.0})

with open("sample.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
