import pytest
import os
from repositories import notification_repository
from repositories.notification_repository import NotificationRepository

TEST_USER_ID = "9999"


@pytest.fixture(scope="module", autouse=True)
def setup_test_notifications_file(tmp_path_factory):
    """
    Create isolated notifications.csv for testing
    """
    test_dir = tmp_path_factory.mktemp("data")
    test_file = test_dir / "notifications.csv"

    # create csv with header
    test_file.write_text(
        "notification_id,user_id,message,type,is_read,created_at\n",
        encoding="utf-8"
    )

    # override file path used by repository
    notification_repository.NOTIFICATIONS_FILE = str(test_file)

    yield

    # cleanup is automatic (tmp directory)


@pytest.fixture
def created_notification():
    NotificationRepository.add_notification(
        user_id=TEST_USER_ID,
        message="Pytest notification",
        notif_type="test"
    )

    notifications = NotificationRepository.get_notifications_by_user(TEST_USER_ID)
    assert len(notifications) > 0

    return notifications[-1]


def test_add_notification(created_notification):
    assert created_notification.user_id == TEST_USER_ID
    assert created_notification.message == "Pytest notification"
    assert created_notification.is_read is False


def test_get_notifications_by_user():
    notifications = NotificationRepository.get_notifications_by_user(TEST_USER_ID)
    assert isinstance(notifications, list)


def test_get_unread_notifications_only(created_notification):
    unread = NotificationRepository.get_notifications_by_user(
        TEST_USER_ID,
        only_unread=True
    )

    assert len(unread) > 0
    for n in unread:
        assert n.is_read is False


def test_mark_as_read(created_notification):
    result = NotificationRepository.mark_as_read(
        created_notification.notification_id
    )

    assert result is True

    notifications = NotificationRepository.get_notifications_by_user(TEST_USER_ID)
    updated = next(
        n for n in notifications
        if str(n.notification_id) == str(created_notification.notification_id)
    )

    assert updated.is_read is True


def test_delete_notification(created_notification):
    result = NotificationRepository.delete_notification(
        created_notification.notification_id
    )

    assert result is True

    notifications = NotificationRepository.get_notifications_by_user(TEST_USER_ID)
    ids = [str(n.notification_id) for n in notifications]

    assert str(created_notification.notification_id) not in ids
