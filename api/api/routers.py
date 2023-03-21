import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from api.models import User, Wallet, User_Pydantic, Wallet_Pydantic
from api.types import Withdraw_Pydantic
from api.settings import settings

from providers.ton_provider import TON_Provider
from utils import encode

router = APIRouter(prefix=settings.API_PREFIX)

TON_API_KEY = [settings.TON_API_KEY_MAINNET,
               settings.TON_API_KEY_TESTNET][settings.TESTNET]


@router.get("/users", tags=['users'])
async def get_all_users():
    response = await User_Pydantic.from_queryset(User.all())
    return {'status': 'ok', 'data': response}


@router.get("/users/{user_id}", tags=['users'])
async def get_user(user_id: int):
    response = await User_Pydantic.from_queryset_single(User.get_or_none(id=user_id))
    return {'status': 'ok', 'data': response}


@router.get("/users/{user_id}/wallets", tags=['users'])
async def get_user_wallets(user_id: int | None = None):
    response = await Wallet_Pydantic.from_queryset(Wallet.filter(user=user_id, is_active=True))
    return {'status': 'ok', 'data': response}


@router.get("/wallets", tags=['wallets'])
async def get_all_wallets():
    response = await Wallet_Pydantic.from_queryset(Wallet.all())
    return {'status': 'ok', 'data': response}


@router.get("/wallets/{wallet_address}", tags=['wallets'])
async def get_wallet(wallet_address: str | None = None):
    response = await Wallet_Pydantic.from_queryset_single(Wallet.get_or_none(address=wallet_address, is_active=True))
    return {'status': 'ok', 'data': response}


@router.get("/images/{image_name}", tags=['images'])
def image_endpoint(image_name: str):
    file_path = f"images/{image_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/svg+xml")
    return {"error": "File not found!"}


@router.post("/withdraw", tags=['transactions'])
async def withdraw(trans: Withdraw_Pydantic):
    trans_dict = trans.dict()

    ton_client = TON_Provider(api_key=TON_API_KEY,
                              testnet=settings.TESTNET)
    from_wallet_address = trans_dict['source']
    # destination_address = await ton_client.get_wallet_info(trans_dict['destination'])
    # if not destination_address.get('wallet'):
    #     return {'error': 'Incorrect address'}

    user_id = trans_dict['user_id']
    user_wallet = await Wallet.get(user=user_id,
                                   address=from_wallet_address,
                                   coin__short_name=trans_dict['coin'],
                                   network__short_name=trans_dict['network'],
                                   )
    if not trans_dict['query_id'] or not user_id:
        return {'error': 'Something was wrong'}

    total_amount = trans_dict['amount'] + trans_dict['gas_fee']
    trans_dict.update({'total': total_amount})

    mnemonic = settings.HOT_WALLET_MNEMONICS.split(',')

    [mnemonics, pub_key, priv_key,
        hot_wallet] = ton_client.get_wallet(mnemonic, version='v3r2')

    if trans_dict['total'] > user_wallet.balance:
        return {'error': 'Not enough money'}
    elif trans_dict['total'] <= user_wallet.min_withdraw_limit:
        return {'error': 'The amount must be more than min withdrawal limit'}

    try:
        msg = f"{from_wallet_address};{trans_dict['total']};{user_id}"

        encoded_msg = encode(msg)
        dest = ton_client.non_bounceable_address(trans_dict['destination'])
        await ton_client.send_tons(hot_wallet,
                                   dest,
                                   trans_dict['amount'],
                                   payload=encoded_msg
                                   )
        user_wallet.balance = user_wallet.balance-total_amount

        await user_wallet.save(update_fields=['balance'])
    except Exception as e:
        return {'error': 'Something was wrong. Try again later'}

    return {'status': 'ok', 'detail': 'Withdraw successful!'}
