
from httpx import AsyncClient
from base64 import b64encode, b64decode

from tonsdk.contract.wallet import Wallets
from tonsdk.crypto import mnemonic_new
from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell

import asyncio


def read_address(cell):
    data = ''.join([str(cell.bits.get(x)) for x in range(cell.bits.length)])
    if len(data) < 267:
        return None
    wc = int(data[3:11], 2)
    hashpart = int(data[11:11+256], 2).to_bytes(32, 'big').hex()
    return Address(f"{wc if wc != 255 else -1}:{hashpart}")


class TON_Provider:
    def __init__(self, api_key, testnet=True):
        self.api_key = api_key
        self.testnet = testnet

        self.client = AsyncClient(headers={'X-API-Key': self.api_key})

    def non_bounceable_address(self, add: str):
         return Address(add).to_string(1, 1, 0)


    async def request(self, method, endpoint, *args, **kwargs):
        response = await self.client.request(
            method, f"https://{'testnet.' if self.testnet else ''}toncenter.com/api/v2/{endpoint}", *args, **kwargs   # noqa: E501
        )
        if response.status_code != 200:
            raise Exception(f"http_code {response.status_code}, response: {response.text}")   # noqa: E501

        return response.json()['result']

    # toncenter methods
    async def send_boc(self, src: bytes):
        return await self.request(
            'POST', 'sendBoc',
            json={
                'boc': b64encode(src).decode(),
            }
        )

    async def get_wallet_info(self, addr: str):
        try:
            return await self.request(
                'GET', 'getWalletInformation',
                params={
                    'address': addr
                }
            )
        except Exception as e:
            print(f"get_wallet_info error: {e}")
            return {}

    async def get_transactions_info(self, addr: str, limit: int = 100):
        try:
            return await self.request(
                'GET', 'getTransactions',
                params={
                    'address': addr,
                    'limit': limit,

                }
            )
        except Exception as e:
            print(f"get_transactions_info error: {e}")
            return {}

    async def get_seqno(self, addr: str):
        try:
            res = await self.get_wallet_info(addr)
            if res['account_state'] == 'uninitialized':
                return 0

            return res.get('seqno', 0)
        except Exception as e:
            print(f"get_seqno error: {e}")
            return 0

    async def run_get_method(self, addr, method, stack=[]):
        try:
            response = await self.request(
                'POST', 'runGetMethod',
                json={
                    'address': addr,
                    'method': method,
                    'stack': stack,
                }
            )
            if response['exit_code'] != 0:
                raise Exception(
                    f"exit_code {response['exit_code']}, response: {response}")

            return response
        except Exception as e:
            if 'exit_code' in f"{e}":
                raise e

            print(f"run_get_method error: {e}")
            await asyncio.sleep(3)
            return await self.run_get_method(addr, method, stack)

    async def get_wallet_address(self, jetton_master_address, owner_address):
        result = await self.run_get_method(jetton_master_address, 'get_wallet_address', [  # noqa: E501
            [
                'tvm.Slice',
                b64encode(
                    begin_cell()
                    .store_address(Address(owner_address))
                    .end_cell().to_boc(False)
                ).decode(),
            ]
        ])

        return read_address(Cell.one_from_boc(b64decode(result['stack'][0][1]['bytes']))).to_string(1, 1, 1)  # noqa: E501

    # wallet methods
    def get_wallet(self, mnemonics=None, version='v3r2', workchain=0):
        if not mnemonics:
            mnemonics = mnemonic_new()

        mnemonics, public_key, private_key, wallet = Wallets.from_mnemonics(
            mnemonics, version=version, workchain=workchain)
        # b64url address may generate `wallet.address.to_string(1, 1, 1)`
        return mnemonics, public_key, private_key, wallet

    async def get_wallet_balances(self, addr, jetton_masters=[]):
        """
        :param jettons: list of jetton master address to get balance
        """

        balances = {
            'ton': int((await self.get_wallet_info(addr)).get('balance', 0),)
        }
        jetton_wallets = {}
        for master_address in jetton_masters:
            try:
                jetton_wallets[
                    (await self.get_wallet_address(master_address, addr))
                ] = master_address
            except Exception as e:
                print(f"get_wallet_balances error: {e}")
                pass

        for wallet_address in jetton_wallets:
            try:
                result = await self.run_get_method(wallet_address, 'get_wallet_data')  # noqa: E501
                balances[
                    jetton_wallets[wallet_address]
                ] = int(result['stack'][0][1], 16)
            except Exception as e:
                print(f"get_wallet_balances error: {e}")
                balances[jetton_wallets[wallet_address]] = 0

        return balances

    async def send_tons(self, wallet, dest: str, amount: int, payload=None,
                        send_mode: int = 1):
        seqno = await self.get_seqno(wallet.address.to_string(1, 1, 1))
        query = wallet.create_transfer_message(
            dest, amount, seqno, payload=payload, send_mode=send_mode
        )
        return await self.send_boc(query['message'].to_boc(False))
