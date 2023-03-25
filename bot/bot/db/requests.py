from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.util._collections import immutabledict
from sqlalchemy import bindparam

from bot.db.models.user import User
from bot.db.models.wallet import (Wallet, Coin,
                                  Network, Transactions)


class DbRequests:
    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id: int):
        async with self.session() as session:
            async with session.begin():
                sql = select(User).where(User.id == user_id)
                request = await session.execute(sql)
                return request.scalar()

    async def get_all_wallets_by_coin(self, coin_name: str):
        async with self.session() as session:
            async with session.begin():
                sql = select(Coin).where(Coin.short_name == coin_name)
                request = await session.execute(sql)
                coin = request.scalar()

                if coin:
                    request = await session.execute(
                        select(Wallet).where(
                            Wallet.coin_id == coin.id)
                    )
                    return request
                else:
                    return False

    async def get_user_wallet(self, user_id: int, network: int):
        async with self.session() as session:
            async with session.begin():
                sql = select(Wallet).where(Wallet.user_id == user_id,
                                           Wallet.network_id == network)
                request = await session.execute(sql)
                return request.scalar()

    async def get_network(self, short_name: str):
        async with self.session() as session:
            async with session.begin():
                sql = select(Network).where(Network.short_name == short_name)
                request = await session.execute(sql)
                return request.scalar()

    async def get_coin(self, short_name: str):
        async with self.session() as session:
            async with session.begin():
                sql = select(Coin).where(Coin.short_name == short_name)
                request = await session.execute(sql)
                return request.scalar()

    async def add_user(self, user_id: int,
                       username: str | None,
                       referral_code: str,
                       invited_by: str | None):
        async with self.session() as session:
            async with session.begin():
                sql = insert(User).values(id=user_id, username=username,
                                          referral_code=referral_code,
                                          invited_by=invited_by).returning('*')

                request = await session.execute(sql)
                await session.commit()
                return request.first()

    async def verify_user(self, user_id: int):
        async with self.session() as session:
            async with session.begin():
                sql = update(User).where(User.id == user_id).values(
                    is_verified=True)
                request = await session.execute(sql)
                await session.commit()
                return request

    async def block_user(self, user_id: int):
        async with self.session() as session:
            async with session.begin():
                sql = update(User).where(User.id == user_id).values(
                    is_verified=False,
                    is_active=False)
                request = await session.execute(sql)
                await session.commit()
                return request

    async def add_user_wallet(self, user_id: int,
                              coin: int, network: int,
                              balance: int,
                              min_withdraw_limit: int,
                              withdrawal_fee: int,
                              address: str,
                              public_key: bytes | str | None,
                              private_key: bytes | str | None,
                              mnemonics: str | None):
        async with self.session() as session:
            sql = insert(Wallet).values(user_id=user_id, coin_id=coin,
                                        balance=balance,
                                        min_withdraw_limit=min_withdraw_limit,
                                        withdrawal_fee=withdrawal_fee,
                                        network_id=network, address=address,
                                        public_key=public_key,
                                        private_key=private_key,
                                        mnemonics=mnemonics
                                        ).returning('*')

            request = await session.execute(sql)
            await session.commit()
            return request.first()

    async def add_network(self, name: str, short_name: str):
        async with self.session() as session:
            sql = insert(Network).values(
                name=name, short_name=short_name).returning('*')

            request = await session.execute(sql)
            await session.commit()
            return request.first()

    async def add_coin(
            self, name: str, short_name: str):
        async with self.session() as session:
            sql = insert(Coin).values(
                name=name,
                short_name=short_name,
                image=f'icon_{short_name.lower()}.svg').returning('*')

            request = await session.execute(sql)
            await session.commit()
            return request.first()

    async def check_transaction(self, body_hash: str, tx_hash: str):
        async with self.session() as session:
            request = await session.execute(
                select(Transactions)
                .where(Transactions.hash == body_hash,
                       Transactions.tx_hash == tx_hash
                       ))
            result = request.first()

        if result:
            return True
        return False

    async def check_wallet(self, address: str):
        async with self.session() as session:
            request = await session.execute(select(Wallet)
                                            .where(Wallet.address == address))
            result = request.first()

        if result:
            return True
        return False

    async def add_v_transaction(self,
                                tx_hash: str,
                                hash: str,
                                incoming_value: int,
                                wallet_id: str,
                                user_id: int,
                                destination: str,
                                sended_amount: int,
                                transaction_type: str,
                                created_time: int
                                ):
        async with self.session() as session:
            sql = insert(Transactions).values(
                tx_hash=tx_hash,
                hash=hash,
                destination_address=destination,
                wallet_id=wallet_id,
                user_id=user_id,
                incoming_value=incoming_value,
                sended_amount=sended_amount,
                transaction_type=transaction_type,
                created_time=created_time
            ).returning('*')
            request = await session.execute(sql)
            await session.commit()
            result = request.first()

        if result:
            return True
        return False

    async def update_balance(self, address: str,
                             balance: int,
                             updated_date: int):
        async with self.session() as session:
            sql = update(Wallet).where(
                Wallet.address == address).values(
                balance=Wallet.balance + balance,
                updated_date=updated_date
            )
            request = await session.execute(
                sql,
                execution_options=immutabledict(
                    {"synchronize_session": 'fetch'})
            )
            await session.commit()
            return request

    async def update_prices(self, params):
        async with self.session() as session:
            sql = (
                insert(Coin).values(
                    short_name=bindparam('_symbol'),
                    price=bindparam('_price'),
                    name=bindparam('_name'),
                    image=bindparam('_img')
                ).on_conflict_do_update(
                    index_elements=['short_name'],
                    set_={
                        'price': bindparam('_price'),
                        'last_updated': bindparam('_utime')
                    }
                )
            )

            request = await session.execute(
                sql,
                params)

            await session.commit()
            return request
