import asyncio
from datetime import datetime

from bot.db.requests import DbRequests, Wallet
from providers.ton_provider import TON_Provider
from utils import encode, decode


async def ton_deposit_watcher(config, session):
    _session = session()
    db = DbRequests(_session)

    TESTNET = config.ton.TESTNET
    TONCENTER_API_KEY = {
        True: config.ton.API_KEY_TESTNET,
        False: config.ton.API_KEY_MAINNET
    }[TESTNET]
    HOT_WALLET = config.ton.HOT_WALLET_ADDRESS

    provider = TON_Provider(TONCENTER_API_KEY, TESTNET)

    while True:
        wallets: list(tuple(Wallet)) = await db.get_all_wallets_by_coin(
            coin_name='TON')

        transactions = await provider.get_transactions_info(HOT_WALLET, limit=5)
        for tx in transactions:
            if not tx['out_msgs']:
                tx_comment = None
                uid = None
                tx_body_hash = tx['in_msg']['body_hash']

                if tx['in_msg']['msg_data'].get('text'):
                    decoded_msg = decode(tx['in_msg']['message'])
                    if decoded_msg:
                        tx_comment = decoded_msg.split(';;')
                        try:
                            uid = int(tx_comment[0])
                            amount = int(tx_comment[1])
                        except Exception:
                            pass

                exist_tx = await db.check_transaction(tx_body_hash, tx['transaction_id'])
                if not exist_tx:
                    wallet = await db.check_wallet(tx['in_msg']['source'])
                    if wallet and uid is not None:
                        val = int(tx['in_msg']['value'])
                        tx_time = datetime.fromtimestamp(tx['utime'])
                        add_tx = await db.add_v_transaction(
                            hash=tx_body_hash,
                            tx_hash=tx['transaction_id'],
                            destination=tx['in_msg']['destination'],
                            incoming_value=val,
                            wallet_id=tx['in_msg']['source'],
                            sended_amount=amount,
                            user_id=uid,
                            transaction_type='DEPOSIT',
                            created_time=tx_time
                        )
                        if add_tx:
                            await db.update_balance(
                                tx['in_msg']['source'],
                                amount,
                                updated_date=tx_time
                            )
                else:
                    continue

        if wallets:
            for _wallet in wallets:
                mnemonics, pub_key, priv_key, wallet = provider.get_wallet(
                    _wallet[0].mnemonics
                )
                wallet_address = wallet.address.to_string(1, 1, 1)

                balances = await provider.get_wallet_balances(wallet_address)

                # print(f"Wallet {wallet_address} balances:")
                # for name in balances:
                #     print(f"\t{name}: {balances[name]}")

                if balances['ton'] > 0:
                    dt = datetime.now()
                    ts = datetime.timestamp(dt)

                    # '{uid};;{amount};;{timestamp}'
                    msg = f'{_wallet[0].user_id};;{balances["ton"]};;{ts}'

                    encoded_msg = encode(msg)

                    # print(f"Sending {balances['ton']} TONs to {HOT_WALLET}")

                    await provider.send_tons(wallet,
                                             HOT_WALLET,
                                             balances['ton'],
                                             payload=encoded_msg)
                    continue

        await asyncio.sleep(50)


async def ton_withdraw_watcher(config, session):
    _session = session()
    db = DbRequests(_session)

    TESTNET = config.ton.TESTNET
    TONCENTER_API_KEY = {
        True: config.ton.API_KEY_TESTNET,
        False: config.ton.API_KEY_MAINNET
    }[TESTNET]
    HOT_WALLET = config.ton.HOT_WALLET_ADDRESS

    provider = TON_Provider(TONCENTER_API_KEY, TESTNET)

    while True:
        transactions = await provider.get_transactions_info(HOT_WALLET)

        for tx in transactions:
            if tx['out_msgs']:
                for out_msg in tx['out_msgs']:
                    tx_comment = None
                    tx_body_hash = out_msg['body_hash']

                    uid = None
                    if out_msg['msg_data'].get('text'):
                        decoded_msg = decode(out_msg['message'])
                        if decoded_msg:
                            tx_comment = decoded_msg.split(';')
                            try:
                                source = tx_comment[0]
                                amount = int(tx_comment[1])
                                uid = int(tx_comment[2])
                            except Exception:
                                pass

                    exist_tx = await db.check_transaction(tx_body_hash, tx['transaction_id'])

                    if not exist_tx and tx_comment is not None:
                        wallet = await db.check_wallet(tx_comment[0])

                        if wallet:
                            val = int(out_msg['value'])
                            tx_time = datetime.fromtimestamp(tx['utime'])
                            await db.add_v_transaction(
                                tx_hash=tx['transaction_id'],
                                hash=tx_body_hash,
                                incoming_value=-val,
                                wallet_id=source,
                                sended_amount=-amount,
                                user_id=uid,
                                transaction_type='WITHDRAW',
                                created_time=tx_time,
                                destination=out_msg['destination']
                            )
                    else:
                        continue

        await asyncio.sleep(10)
