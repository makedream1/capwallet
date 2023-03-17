from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from bot.db.requests import DbRequests
from providers.ton_provider import TON_Provider


class TONMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, api_key, testnet=True):
        super().__init__()
        self.api_key = api_key
        self.testnet = testnet

    async def pre_process(self, obj, data, *args):
        db_request: DbRequests = data['db_request']
        self.provider = TON_Provider(self.api_key, self.testnet)

        self.coin = await db_request.get_coin('TON')
        self.network = await db_request.get_network('TON')
        if not self.coin:
            await db_request.add_coin('Toncoin', 'TON')
        if not self.network:
            await db_request.add_network('The Open Network', 'TON')

    async def post_process(self, obj, data, *args):
        db_request: DbRequests = data['db_request']
        user_id = obj.from_user
        user = await db_request.get_user(user_id)

        wallet = None

        if self.network:
            wallet = await db_request.get_user_wallet(user_id, self.network.id)

        if user.is_verified:
            if not wallet:
                mnemonics, public_key, private_key, new_wallet = self.provider.get_wallet()  # noqa: E501
                wallet_address = new_wallet.address.to_string(1, 1, 1)
                min_withdraw_limit = 100_000_000
                withdrawal_fee = 50_000_000
                balances = await self.provider.get_wallet_balances(
                    wallet_address)
                wallet = await db_request.add_user_wallet(
                    user_id=user_id,
                    network=self.network.id,
                    coin=self.coin.id,
                    balance=balances['ton'],
                    min_withdraw_limit=min_withdraw_limit,
                    withdrawal_fee=withdrawal_fee,
                    address=wallet_address,
                    public_key=public_key.hex(),
                    private_key=private_key.hex(),
                    mnemonics=mnemonics
                )
