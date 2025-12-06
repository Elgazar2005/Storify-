class Notification:
    def __init__(self, notification_id, user_id, message, type, is_read, created_at):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.type = type
        self.is_read = is_read
        self.created_at = created_at