import csv
from models.user import User

class UserRepository:
    FILE_PATH = "data/users.csv"
    FIELDNAMES = ["id", "username", "email", "password", "role", "store_name"]

    def __init__(self, file_singleton):
        # هنا بنستقبل الـ singleton من الـ factory
        self.file = file_singleton

    def get_all(self):
        users = []
        try:
            rows = self.file.read_csv(self.FILE_PATH)
            for row in rows:
                users.append(User(
                    id=int(row["id"]),
                    username=row["username"],
                    email=row["email"],
                    password=row["password"],
                    role=row.get("role", "customer"),
                    store_name=row.get("store_name", "")
                ))
        except FileNotFoundError:
            pass
        return users

    def get_by_id(self, user_id):
        for user in self.get_all():
            if user.id == user_id:
                return user
        return None

    def create_user(self, username, email, password, role, store_name=""):
        users = self.get_all()
        new_id = 1 if not users else users[-1].id + 1

        new_user = User(
            id=new_id,
            username=username,
            email=email,
            password=password,
            role=role,
            store_name=store_name
        )

        self.file.append_csv(
            self.FILE_PATH,
            self.FIELDNAMES,
            new_user.to_dict()
        )

        return new_user
