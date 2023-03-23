import asyncio
from datetime import datetime

from aiohttp import ClientSession

from bot.db.requests import DbRequests


async def update_prices(config, session):
    _session = session()
    db = DbRequests(_session)

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api_key = config.coinmarketcap.COINMARKETCAP_API_KEY

    parameters = {
        'symbol': 'TON,USDT,DAI,NEAR,USDC,BUSD',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    while True:
        async with ClientSession() as session:
            session.headers.update(headers)
            coin = await db.get_coin('TON')
            now = datetime.utcnow()
            delta = now - coin.last_updated

            if delta.total_seconds() > 300:
                async with session.get(url, params=parameters) as response:
                    info = await response.json()
                    data = info['data']
                    coins = []
                    for key in data:
                        coins.append({
                            '_symbol': key,
                            '_name': data[key]['name'],
                            '_price': round(
                                data[key]['quote']['USD']['price'],
                                2),
                            '_img': f'icon_{key}.svg'.lower(),
                            '_utime': datetime.utcnow()
                        })
                    await db.update_prices(params=coins)

        await asyncio.sleep(300)
