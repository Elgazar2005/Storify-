from Models.Notification import Notification

def test_notification_creation():
    notif = Notification(1, 2, "Hello", "general", False, "2024-01-01")

    assert notif.notification_id == 1
    assert notif.user_id == 2
    assert notif.message == "Hello"
    assert notif.is_read is False

def test_notification_repr():
    notif = Notification(1, 2, "Hello", "general", False, "2024-01-01")
    assert repr(notif) == "<Notification 1 to User 2>"