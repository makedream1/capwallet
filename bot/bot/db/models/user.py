from sqlalchemy import (
    Column, BigInteger, String,
    Boolean, DateTime, func)
from sqlalchemy.orm import relationship

from bot.db.base import BaseModel


class User(BaseModel):
    __tablename__ = "User"

    id = Column(BigInteger, primary_key=True,
                unique=True, autoincrement=False)

    username = Column(String)
    referral_code = Column(String)
    invited_by = Column(String)

    is_admin = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_date = Column(DateTime, default=func.now())

    wallets = relationship(
        "Wallet",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
