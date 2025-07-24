# server/graphql/permissions.py
from typing import Any
from strawberry.permission import BasePermission
from strawberry.types import Info

class IsAuthenticated(BasePermission):
    message = "Authorization required"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return info.context.get("current_client") is not None

class IsClientOwner(BasePermission):
    message = "You do not have permission to modify this client"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        client = info.context.get("current_client")
        input_data = kwargs.get("input")
        target_id = getattr(input_data, "id", None)
        print(client.id, target_id)
        return bool(client and str(client.id) == str(target_id))