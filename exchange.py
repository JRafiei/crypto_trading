from abc import ABC, abstractmethod
from typing import Dict
from models import Order


class Exchange(ABC):
    """Base Interface for implementing exchanges"""

    def __init__(self, name: str, base_url: str) -> None:
        self.name = name
        self.base_url = base_url

    @abstractmethod
    def login(self, **credentials) -> str:
        """Login with credentials and return a token"""
        pass

    @abstractmethod
    def add_order(order: Order) -> dict:
        """Submit an order in the exchange's orderbook"""
        pass

    @abstractmethod
    def get_current_prices(self, dst_currency: str) -> dict:
        """Get current prices as a dict of currencies"""
        pass

    @abstractmethod
    def get_orderbook(self, symbol: str) -> dict:
        """Get orderbook for a specific currency"""
        pass

    @abstractmethod
    def get_wallets(self) -> dict:
        """Get wallets data of the user"""
        pass
