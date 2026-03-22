from .admin_message import router as admin_message_router
from .admin_register import router as admin_register_router
from .superuser_menu import router as superuser_menu_router

__all__ = (
    "admin_message_router",
    "admin_register_router",
    "superuser_menu_router",
)