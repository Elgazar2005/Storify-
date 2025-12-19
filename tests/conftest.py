import pytest
import sys
import os
from app import app as flask_app
from core.file_singletone import FileSingleton
from repositories import (
    order_repository,
    notification_repository,
    product_repository,
    user_repository,
    cart_repository
)
