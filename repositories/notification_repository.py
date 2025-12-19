from datetime import datetime
from core.file_singletone import FileSingleton
from Models.Notification import Notification

NOTIFICATIONS_FILE = "notifications.csv"


class NotificationRepository:
    file = FileSingleton()
    @staticmethod
    def get_all_notifications():
        rows = NotificationRepository.file.read_csv(NOTIFICATIONS_FILE)
        notifications = []
        for row in rows:
            notification = Notification(
                notification_id=row["notification_id"],
                user_id=row["user_id"],
                message=row["message"],
                type=row["type"],
                is_read=row["is_read"] == "True",
                created_at=row["created_at"]
            )
            notifications.append(notification)

        return notifications

    @staticmethod
    def get_notifications_by_user(user_id, only_unread=False):
        notifications = NotificationRepository.get_all_notifications()
        result = []
        for n in notifications:
            if n.user_id == str(user_id):
                if only_unread:
                    if n.is_read is False:
                        result.append(n)
                else:
                    result.append(n)
        return result
    @staticmethod
    def add_notification(user_id, message, notif_type="general"):
        new_id = NotificationRepository._get_next_id()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        fieldnames = [
            "notification_id",
            "user_id",
            "message",
            "type",
            "is_read",
            "created_at"
        ]

        NotificationRepository.file.append_csv(
            NOTIFICATIONS_FILE,
            fieldnames,
            {
                "notification_id": new_id,
                "user_id": user_id,
                "message": message,
                "type": notif_type,
                "is_read": "False",
                "created_at": created_at
            }
        )

    @staticmethod
    def mark_as_read(notification_id):
        notifications = NotificationRepository.get_all_notifications()

        for n in notifications:
            if str(n.notification_id) == str(notification_id):
                n.is_read = True
                NotificationRepository._save_all(notifications)
                return True

        return False
    @staticmethod
    def delete_notification(notification_id):
        notifications = NotificationRepository.get_all_notifications()
        new_list = []

        deleted = False

        for n in notifications:
            if str(n.notification_id) == str(notification_id):
                deleted = True
            else:
                new_list.append(n)

        if deleted:
            NotificationRepository._save_all(new_list)

        return deleted
    @staticmethod
    def _get_next_id():
        notifications = NotificationRepository.get_all_notifications()
        if len(notifications) == 0:
            return 1
        max_id = 0
        for n in notifications:
            if int(n.notification_id) > max_id:
                max_id = int(n.notification_id)
        return max_id + 1
    @staticmethod
    def _save_all(notifications):
        fieldnames = [
            "notification_id",
            "user_id",
            "message",
            "type",
            "is_read",
            "created_at"
        ]

        rows = []

        for n in notifications:
            row = {
                "notification_id": n.notification_id,
                "user_id": n.user_id,
                "message": n.message,
                "type": n.type,
                "is_read": str(n.is_read),
                "created_at": n.created_at
            }
            rows.append(row)

        NotificationRepository.file.write_csv(
            NOTIFICATIONS_FILE,
            fieldnames,
            rows
        )
