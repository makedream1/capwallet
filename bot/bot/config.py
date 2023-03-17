from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str


@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class TONConfig:
    TESTNET: bool
    API_KEY_TESTNET: str
    API_KEY_MAINNET: str
    HOT_WALLET_ADDRESS: str
    HOT_WALLET_MNEMONICS: list


@dataclass
class CoinMarketCapConfig:
    COINMARKETCAP_API_KEY: str


@dataclass
class Config:
    bot: BotConfig
    db: DatabaseConfig
    ton: TONConfig
    coinmarketcap: CoinMarketCapConfig


def load_config(path: str | None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        bot=BotConfig(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS"))),
            use_redis=env.bool("USE_REDIS")
        ),
        db=DatabaseConfig(
            db_host=env.str("DB_HOST"),
            db_password=env.str("DB_PASS"),
            db_user=env.str("DB_USER"),
            database=env.str("DB_NAME")
        ),
        ton=TONConfig(
            TESTNET=env.bool("TESTNET"),
            API_KEY_TESTNET=env.str("TON_API_KEY_TESTNET"),
            API_KEY_MAINNET=env.str("TON_API_KEY_MAINNET"),
            HOT_WALLET_ADDRESS=env.str("HOT_WALLET_ADDRESS"),
            HOT_WALLET_MNEMONICS=env.str("HOT_WALLET_MNEMONICS")
        ),
        coinmarketcap=CoinMarketCapConfig(
            COINMARKETCAP_API_KEY=env.str("COINMARKETCAP_API_KEY")
        )
    )
