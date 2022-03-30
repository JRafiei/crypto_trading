from dataclasses import dataclass


@dataclass
class Order:
    type: str
    amount: float
    price: float
    src_currency: str
    dst_currency: str = "usdt"
