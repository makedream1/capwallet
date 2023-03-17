from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from api.settings import settings
from api.routers import router


app = FastAPI(title="WALLET_API")

app.include_router(router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

DATABASE_URL = f"asyncpg://{settings.db_user}:{settings.db_password}@postgres:5432/{settings.database}"

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["api.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)
