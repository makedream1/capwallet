from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

from bot.db.models.wallet import Wallet, Network, Coin   # noqa: F401,E402
from bot.db.models.user import User                      # noqa: F401,E402
