import csv
from Models.Notification import Notification
from datetime import datetime

NOTIFICATIONS_FILE = "notifications.csv"

class NotificationRepository:

    @staticmethod
    def get_all_notifications():
        notifications = [] #empty to store data of file
        try:
            with open(NOTIFICATIONS_FILE, mode="r", newline="", encoding="utf-8") as file: # open file csv in read mode
                reader = csv.DictReader(file) #change file to dictonary
                for row in reader:
                    # make opeject of notification that story each row  and after that put it in empty list
                   notifications.append(Notification(
                        notification_id=row["notification_id"],
                        user_id=row["user_id"],
                        message=row["message"],
                        type=row["type"],
                        is_read=row["is_read"] == "True",
                        created_at=row["created_at"]
                    ))
        except FileNotFoundError: # we use this to check if file is here or not if here use try if isnot go to bulid in function is
            #not found and not return notification
            pass
        return notifications

    @staticmethod
    def get_notifications_by_user(user_id, only_unread=False): #this function take ID and unread if there is no parmeter it be false
        notifications = NotificationRepository.get_all_notifications() #this get all notification from file
        user_notifications = [n for n in notifications if n.user_id == str(user_id)] #this loop compare user in file with user id that in and change that user enter to string  
        if only_unread:# this check if only_unread==true change user_notification save that statues==unread
            user_notifications = [n for n in user_notifications if n.status == "unread"]
        return user_notifications

    @staticmethod
    def add_notification(user_id, message, notif_type="general"):#this function is used to addnew_notif
        new_id = NotificationRepository._get_next_id() #make new id to the ne notification
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")#put the exactly time that created notification
        new_notification = Notification(
            notification_id=new_id,
            user_id=user_id,
            message=message,
            type=notif_type,
            is_read=False,
            created_at=created_at
        ) #create the object

        fieldnames = ["notification_id","user_id","message","type","is_read","created_at"]
        try:
            with open(NOTIFICATIONS_FILE, mode="a", newline="", encoding="utf-8") as file: #open file in mode append write
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0: #this if condition is check if file is empty to rewrite the headers before add
                    writer.writeheader()
                writer.writerow({ #this add data to file
                    "notification_id": new_notification.notification_id,
                    "user_id": new_notification.user_id,
                    "message": new_notification.message,
                    "type": new_notification.type,
                    "is_read": str(new_notification.is_read),
                    "created_at": new_notification.created_at
                })
        except Exception as e: #if there is any error is print to me and make the project running without stop
            print("Error writing notification:", e)
        return new_notification

    @staticmethod
    def mark_as_read(notification_id): #this function is used to change is_read to True
        notifications = NotificationRepository.get_all_notifications()
        updated = False
        for n in notifications:
            if str(n.notification_id) == str(notification_id):
                n.is_read = True
                updated = True
                break
        if updated:# save data if update change to true and then save
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
        notifications = NotificationRepository.get_all_notifications() #get all data from file as dicnary
        if notifications: #check if notification is not empty
            return max(int(n.id) for n in notifications) + 1 #get max number and increase 1 to make new id
        return 1

    @staticmethod
    def _save_all(notifications):
        fieldnames = ["notification_id","user_id","message","type","is_read","created_at"]
        try:
            with open(NOTIFICATIONS_FILE, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for n in notifications:
                    writer.writerow({
                        "notification_id": n.notification_id,
                        "user_id": n.user_id,
                        "message": n.message,
                        "type": n.type,
                        "is_read": str(n.is_read),
                        "created_at": n.created_at
                    })
        except Exception as e:
            print("Error saving notifications:", e)
