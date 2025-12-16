import csv
from Models.Notification import Notification
from core.file_singletone import FileSingleton
from datetime import datetime

NOTIFICATIONS_FILE = "notifications.csv"

class NotificationRepository:
    file = FileSingleton() # make object from singltone to make one connection with database

    @staticmethod
    def get_all_notifications():
        rows = NotificationRepository.file.read_csv(NOTIFICATIONS_FILE) #Read rows of file notification    
        notifications = [] # empty list []

        for row in rows:
            notifications.append(Notification( # here we take each element and put it in empty list 
                notification_id=row["notification_id"],
                user_id=row["user_id"],
                message=row["message"],
                type=row["type"],
                is_read=row["is_read"] == "True",
                created_at=row["created_at"]
            ))
        return notifications

    @staticmethod
    def get_notifications_by_user(user_id, only_unread=False): # get notification by specific user by id
        notifications = NotificationRepository.get_all_notifications() #store all notification to make after that filiteration
        user_notifications = [n for n in notifications if n.user_id == str(user_id)] #make for loop to all users to get the specific user that we need

        if only_unread:# filter all unread and appear it
            user_notifications = [n for n in user_notifications if n.status == "unread"]

        return user_notifications

    @staticmethod #Function to create a new notification
    def add_notification(user_id, message, notif_type="general"): #
        new_id = NotificationRepository._get_next_id() # this function is help_function the generate id by assecnding to add new id to new notif 
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # this function is used to get the specific time 

        new_notification = Notification( # this add new notification 
            notification_id=new_id,
            user_id=user_id,
            message=message,
            type=notif_type,
            is_read=False,
            created_at=created_at
        )

        fieldnames = ["notification_id", "user_id", "message", "type", "is_read", "created_at"]

        try:
            NotificationRepository.file.append_csv( #append this to the file csv
                NOTIFICATIONS_FILE,
                {
                    "notification_id": new_notification.notification_id,
                    "user_id": new_notification.user_id,
                    "message": new_notification.message,
                    "type": new_notification.type,
                    "is_read": str(new_notification.is_read),
                    "created_at": new_notification.created_at
                },
                fieldnames
            )
        except Exception as e:
            print("Error writing notification:", e)

        return new_notification

    @staticmethod
    def mark_as_read(notification_id): #this function is used make the messge is read
        notifications = NotificationRepository.get_all_notifications()
        updated = False

        for n in notifications:
            if str(n.notification_id) == str(notification_id):
                n.is_read = True
                updated = True
                break

        if updated: #after that save it
            NotificationRepository._save_all(notifications)

        return updated

    @staticmethod
    def delete_notification(notification_id): 
        notifications = NotificationRepository.get_all_notifications()
        deleted = False

        for n in notifications:
            if str(n.notification_id) == str(notification_id):
                notifications.remove(n)
                deleted = True
                break

        if deleted:
            NotificationRepository._save_all(notifications)

        return deleted

    @staticmethod
    def _get_next_id():
        notifications = NotificationRepository.get_all_notifications()
        if notifications:
            return max(int(n.id) for n in notifications) + 1
        return 1

    @staticmethod
    def _save_all(notifications):
        fieldnames = ["notification_id", "user_id", "message", "type", "is_read", "created_at"]

        rows = []
        for n in notifications:
            rows.append({
                "notification_id": n.notification_id,
                "user_id": n.user_id,
                "message": n.message,
                "type": n.type,
                "is_read": str(n.is_read),
                "created_at": n.created_at
            })

        NotificationRepository.file.write_csv(NOTIFICATIONS_FILE, rows, fieldnames)
