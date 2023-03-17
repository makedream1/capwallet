from pydantic import BaseModel


class Withdraw_Pydantic(BaseModel):
    query_id: str
    user_id: int
    source: str
    amount: int
    gas_fee: int
    destination: str
    coin: str
    network: str
