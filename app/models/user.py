import typing
from aiogram.utils.markdown import hlink, hbold

from sqlalchemy.sql import Select, expression
from sqlalchemy.dialects.postgresql import UUID

from app.loader import db
from app.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    is_superuser = db.Column(db.Boolean, server_default=expression.false())
    balance = db.Column(db.Integer, server_default='0')
    referral_id = db.Column(db.Integer, nullable=True)
    code = db.Column(UUID(), nullable=True, server_default=expression.null())

    query: Select

    @property
    def has_access(self) -> bool:
        return bool(self.is_superuser or self.referral_id)

    @property
    def preview(self) -> str:
        access = ''
        if self.referral_id:
            access = 'Ваш реферал: ' + hlink(title=f"ID:{self.referral_id}",
                                             url=f"tg://user?id={self.referral_id}")
        elif self.is_superuser:
            access = hbold('Вы являетесь администратором')

        preview = ' \n'.join((
            f'🆔 Ваш id: {self.id}',
            f'💵 Ваш баланс: ${self.balance / 100} USD',
            f'🍻 {access}',
        ))
        return preview

    @staticmethod
    async def add_superusers(superuser_ids: typing.Union[typing.List[typing.Union[str, int]], typing.Union[str, int]]):
        if isinstance(superuser_ids, str):
            superuser_ids = [superuser_ids]

        for user_id in map(int, superuser_ids):
            user = await User.get(user_id)
            if not user:
                await User.create(id=user_id, is_superuser=True)
            else:
                await user.update(is_superuser=True).apply()

    @staticmethod
    async def remove_superusers(superuser_ids: typing.Union[typing.List[typing.Union[str, int]], typing.Union[str, int]]):
        if isinstance(superuser_ids, str):
            superuser_ids = [superuser_ids]

        for user_id in map(int, superuser_ids):
            user = await User.get(user_id)
            await user.update(is_superuser=False).apply()


class UserRelatedMixin:
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
