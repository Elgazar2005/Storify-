import csv

class FileSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileSingleton, cls).__new__(cls)
        return cls._instance

    def read_csv(self, path):
        with open(path, newline='', encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def write_csv(self, path, fieldnames, rows):
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def append_csv(self, path, fieldnames, row):
        with open(path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(row)
