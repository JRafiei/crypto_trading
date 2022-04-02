from dataclasses import dataclass


@dataclass
class Order:
    type: str
    amount: float
    price: float
    condition: str
    src_currency: str
    dst_currency: str = "usdt"

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "price": self.price,
            "condition": self.condition,
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
