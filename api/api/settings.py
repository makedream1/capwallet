from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    bot_token: str = Field(..., env='BOT_TOKEN')
    admin_ids: str = Field(..., env='ADMIN_IDS')
    use_redis: bool = Field(..., env='USE_REDIS')

    db_password: str = Field(..., env='DB_PASS')
    db_user: str = Field(..., env='DB_USER')
    database: str = Field(..., env='DB_NAME')

    TESTNET: bool = Field(..., env='TESTNET')
    TON_API_KEY_TESTNET: str = Field(..., env='TON_API_KEY_TESTNET')
    TON_API_KEY_MAINNET: str = Field(..., env='TON_API_KEY_MAINNET')
    HOT_WALLET_ADDRESS: str = Field(..., env='HOT_WALLET_ADDRESS')
    HOT_WALLET_MNEMONICS: str = Field(..., env='HOT_WALLET_MNEMONICS')


    API_PREFIX: str = Field(..., env='API_PREFIX')
    HOST_URL: str = Field(..., env='HOST_URL')

    COINMARKETCAP_API_KEY: str = Field(..., env='COINMARKETCAP_API_KEY')

    class Config:
      env_file = '.env'
      env_file_encoding = 'utf-8'


settings = Settings()