import pytest
from datetime import datetime
from repositories import order_repository, notification_repository
from repositories.order_repository import OrderRepository
from Models.order import Order
from Models.orderitem import OrderItem


@pytest.fixture(scope="module", autouse=True)
def setup_test_files(tmp_path_factory):
    """
    Create isolated CSV files for orders, order_items, notifications
    """
    test_dir = tmp_path_factory.mktemp("data")

    orders_file = test_dir / "orders.csv"
    order_items_file = test_dir / "order_items.csv"
    notifications_file = test_dir / "notifications.csv"

    orders_file.write_text(
        "order_id,customer_id,created_at,status,total_amount\n",
        encoding="utf-8"
    )
    order_items_file.write_text(
        "order_item_id,order_id,product_id,product_name,quantity,price,seller_id\n",
        encoding="utf-8"
    )
    notifications_file.write_text(
        "notification_id,user_id,message,type,is_read,created_at\n",
        encoding="utf-8"
    )

    order_repository.ORDERS_FILE = str(orders_file)
    order_repository.ORDER_ITEMS_FILE = str(order_items_file)
    notification_repository.NOTIFICATIONS_FILE = str(notifications_file)

    yield


@pytest.fixture
def sample_order():
    return Order(
        order_id="1",
        customer_id="100",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status="pending",
        total_amount="500"
    )


@pytest.fixture
def sample_order_item():
    return OrderItem(
        order_item_id="1",
        order_id="1",
        product_id="10",
        product_name="Test Product",
        quantity=5,
        price=100.0,
        seller_id="200"
    )


def test_add_and_get_orders(sample_order):
    OrderRepository.add_order(sample_order)

    orders = OrderRepository.get_all_orders()

    assert len(orders) == 1
    assert orders[0].order_id == "1"
    assert orders[0].status == "pending"


def test_add_and_get_order_items(sample_order_item):
    OrderRepository.add_order_item(sample_order_item)

    items = OrderRepository.get_all_order_items()

    assert len(items) == 1
    assert items[0].product_name == "Test Product"
    assert items[0].quantity == 5


def test_update_order_item_quantity_triggers_notification(sample_order_item):
    updated = OrderRepository.update_order_item_quantity(
        order_item_id="1",
        new_quantity=2
    )

    assert updated is True

    items = OrderRepository.get_all_order_items()
    assert items[0].quantity == 2

    notifications = notification_repository.NotificationRepository.get_notifications_by_user("200")
    assert len(notifications) > 0
    assert notifications[-1].type == "low_stock"


def test_update_order_status(sample_order):
    updated = OrderRepository.update_order_status(
        order_id="1",
        new_status="shipped"
    )

    assert updated is True

    orders = OrderRepository.get_all_orders()
    assert orders[0].status == "shipped"
