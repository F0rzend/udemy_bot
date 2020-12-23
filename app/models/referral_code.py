from uuid import uuid4

from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.markdown import hlink

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import Select

from app import models
from app.models.base import TimedBaseModel
from app.models.user import UserRelatedMixin, User
from app.loader import db


class ReferralCode(TimedBaseModel, UserRelatedMixin):
    __tablename__ = "referral_codes"

    code = db.Column(UUID(), primary_key=True, unique=True, index=True, nullable=True, default=uuid4)
    query: Select

    _user: models.User

    async def get_users(self):
        return await User.query.where(code=self.code).gino.all()

    @property
    async def preview(self):
        preview = hlink(title=str(self.code), url=await self.deeplink)
        return preview

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    async def deeplink(self):
        return await get_start_link(f'code__{self.code}', encode=True)
