import logging
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models.user import User
from bot.db.requests import DbRequests


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session: AsyncSession = session

    async def pre_process(self, obj, data, *args):
        session = self.session()
        data["session"] = session
        db_request = DbRequests(session)
        data["db_request"] = db_request
        from_user = obj.from_user
        user = await session.get(User, from_user.id)

        if not user:
            invite_code = obj.text.split()
            invited_by = invite_code[1][1:] if len(invite_code) > 1 else None

            await db_request.add_user(user_id=from_user.id,
                                      username=from_user.username,
                                      referral_code=f'r{from_user.id}',
                                      invited_by=invited_by)

            logging.info(f"new user {from_user.full_name} in db")

    async def post_process(self, obj, data, *args):
        session = data.get("session")
        if session:
            await session.close()
