from sqlalchemy import (
    Column, BigInteger, String, ForeignKey, Float,
    Boolean, DateTime, func)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from bot.db.base import BaseModel


class Wallet(BaseModel):
    __tablename__ = "Wallet"

    address = Column(String, primary_key=True,
                     unique=True)
    user_id = Column(BigInteger, ForeignKey("User.id"))

    balance = Column(BigInteger, default=0, nullable=False)
    min_withdraw_limit = Column(BigInteger, default=0, nullable=False)
    withdrawal_fee = Column(BigInteger, default=0, nullable=False)

    network_id = Column(BigInteger, ForeignKey("Network.id"))
    coin_id = Column(BigInteger, ForeignKey("Coin.id"))

    public_key = Column(String)
    private_key = Column(String)
    mnemonics = Column(ARRAY(String), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="wallets")


class Network(BaseModel):
    __tablename__ = 'Network'

    id = Column(BigInteger, primary_key=True,
                unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    short_name = Column(String, unique=True, nullable=False)


class Coin(BaseModel):
    __tablename__ = 'Coin'

    id = Column(BigInteger, primary_key=True,
                unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    short_name = Column(String, unique=True, nullable=False)
    price = Column(Float, default=0, nullable=False)
    image = Column(String, default="", nullable=False)
    last_updated = Column(DateTime, default=func.now())


class Transactions(BaseModel):
    __tablename__ = 'Transactions'

    hash = Column(String, primary_key=True, unique=True, nullable=False)
    destination_address = Column(String, nullable=False)
    wallet_id = Column(String, ForeignKey("Wallet.address"))
    user_id = Column(BigInteger, ForeignKey("User.id"))

    incoming_value = Column(BigInteger, nullable=False)
    sended_amount = Column(BigInteger, default=0, nullable=False)

    transaction_type = Column(String)  # deposit or withdraw
    created_time = Column(DateTime, default=func.now())
