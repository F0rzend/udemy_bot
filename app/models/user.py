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


class UserRelatedMixin:
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
