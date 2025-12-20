import csv
from Models.user import User
from core.file_singletone import FileSingleton

class UserRepository:
    file = FileSingleton()
    FILE_PATH = "data/users.csv"

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
            return []
        return users

    def get_by_id(self, user_id):
        for user in self.get_all():
            if int(user.id) == int(user_id):
                return user
        return None

    def create_user(self, username, email, password, role, store_name=""):
        users = self.get_all()

        # generate new ID
        new_id = 1 if not users else users[-1].id + 1

        new_user = User(
            id=new_id,
            username=username,
            email=email,
            password=password,
            role=role,
            store_name=store_name
        )

        # write row using Singleton
        self.file.append_csv(
            self.FILE_PATH,
            ["id", "username", "email", "password", "role", "store_name"],
            new_user.to_dict()
        )

        return new_user
