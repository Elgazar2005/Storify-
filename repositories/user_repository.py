import csv
from Models.user import User

class UserRepository:
    def __init__(self, file_path="data/users.csv"):
        self.file_path = file_path

    def get_all(self):
        users = []
        with open(self.file_path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(User(
                    id=row["id"],
                    username=row["username"],
                    email=row["email"],
                    password=row["password"],
                    role=row["role"]
                ))
        return users

    def get_by_id(self, user_id):
        for user in self.get_all():
            if user.id == int(user_id):
                return user
        return None
