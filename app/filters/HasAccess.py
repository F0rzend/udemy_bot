from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from app.models.user import User


@dataclass
class HasAccess(BoundFilter):
    has_access: bool

    key = "has_access"
    required = True
    default = True

    async def check(self, obj) -> bool:
        data = ctx_data.get()
        user: User = data["user"]
        return self.has_access == user.has_access
