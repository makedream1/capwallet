from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.exceptions import NoValuesFetched

from api.settings import settings


class User(models.Model):
    """
    The User model
    """

    id = fields.BigIntField(pk=True)
    is_verified = fields.BooleanField()
    is_active = fields.BooleanField()

    def __str__(self) -> str:
        return f'{self.id}'

    def total_balance(self) -> float:
        total_balance: float = 0.0
        try:
            if self.wallets:
                for wallet in self.wallets:
                    balance = wallet.balance
                    if wallet.coin.short_name == 'TON':
                        balance = wallet.balance / 1e9
                    price = wallet.coin.price
                    usd_balance = price * balance

                    total_balance += usd_balance
        except NoValuesFetched:
            pass

        return total_balance

    class Meta:
        table: str = 'User'

    class PydanticMeta:
        exclude = ['is_verified', 'user_transactions']
        computed = ['total_balance']


class Coin(models.Model):
    """
    The Coin model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    short_name = fields.CharField(max_length=10)
    price = fields.FloatField(default=0, null=False)
    image = fields.CharField(max_length=1000)
    last_updated = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_image(self) -> str:
        return f"{settings.HOST_URL}{settings.API_PREFIX}/images/{self.image}"

    class Meta:
        table: str = 'Coin'

    class PydanticMeta:
        exclude = ['id']
        computed = ["get_image"]


class Network(models.Model):
    """
    The Network model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    short_name = fields.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    class Meta:
        table: str = 'Network'

    class PydanticMeta:
        exclude = ['id']


class Wallet(models.Model):
    """
    The Wallet model
    """

    address = fields.CharField(pk=True, max_length=80, unique=True, null=False)
    user = fields.ForeignKeyField(
        model_name="models.User", related_name='wallets')
    balance = fields.BigIntField(default=0, null=False)
    min_withdraw_limit = fields.BigIntField(default=0, null=False)
    withdrawal_fee = fields.BigIntField(default=0, null=False)
    mnemonics = ArrayField(element_type="text")
    network: fields.ForeignKeyRelation[Network] = fields.ForeignKeyField(
        "models.Network", related_name="wallet_network")
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField(
        "models.Coin", related_name="wallet_coin")

    is_active = fields.BooleanField()
    updated_date = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.address

    def wallet_balance(self) -> float:
        balance = self.balance
        if self.coin.short_name == 'TON':
            balance = self.balance / 1e9
        return balance

    class Meta:
        table: str = 'Wallet'

    class PydanticMeta:
        computed = ['wallet_balance']
        exclude = ['user', 'is_active', 'mnemonics']


class Transactions(models.Model):
    """
    The Transactions model
    """

    hash = fields.CharField(pk=True, max_length=80, null=False, unique=True)
    destination_address = fields.CharField(max_length=100, null=False)
    wallet = fields.ForeignKeyField(
        model_name="models.Wallet", field_to="address", related_name='wallet_transactions')
    user = fields.ForeignKeyField(
        model_name="models.User", related_name='user_transactions')

    incoming_value = fields.BigIntField(default=0)
    sended_amount = fields.BigIntField(default=0)

    transaction_type = fields.CharField(max_length=20)
    created_time = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.hash}'

    class Meta:
        table: str = 'Transactions'

    class PydanticMeta:
        exclude = ['user', 'incoming_value']


Tortoise.init_models(['api.models'], 'models')

User_Pydantic = pydantic_model_creator(User, name="User")
Coin_Pydantic = pydantic_model_creator(Coin, name="Coin")
Network_Pydantic = pydantic_model_creator(Network, name="Network")
Wallet_Pydantic = pydantic_model_creator(Wallet, name="Wallet")
Transactions_Pydantic = pydantic_model_creator(
    Transactions, name="Transactions")
