from dataclasses import dataclass
from datetime import datetime
from bson import ObjectId


@dataclass
class Order:
    _id: ObjectId
    type: str
    amount: float
    price: float
    condition: str
    created_at: datetime
    src_currency: str
    dst_currency: str = "usdt"
    status: str = "pending"

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "price": self.price,
            "condition": self.condition,
            "status": self.status,
            "created_at": self.created_at,
            "src_currency": self.src_currency,
            "dst_currency": self.dst_currency,
        }


@dataclass
class Notification:
    type: str
    price: float
    condition: str
    currency: str

    def to_dict(self):
        return {
            "type": self.type,
            "price": self.price,
            "condition": self.condition,
            "currency": self.currency,
        }
