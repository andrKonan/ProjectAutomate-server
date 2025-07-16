# server/utils/permissions.py
from typing import Any
from strawberry.permission import BasePermission
from strawberry.types import Info

class IsAuthenticated(BasePermission):
    message = "Authentication required"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        # simply block if there's no current_client in our context
        return info.context.get("current_client") is not None

class IsClientOwner(BasePermission):
    message = "You do not have permission to modify this client"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        # kwargs contains your resolver arguments—so grab the `id` arg
        client = info.context.get("current_client")
        target_id = kwargs.get("id")
        return bool(client and str(client.id) == str(target_id))