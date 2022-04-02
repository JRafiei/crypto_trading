import json
import requests
from exchange import Exchange
from order import Order


class NobitexExchange(Exchange):

    def __init__(self) -> None:
        super().__init__(name='nobitex', base_url='https://api.nobitex.ir')
        self.src_currencies = [
            'btc', 'ltc', 'bnb', 'eth', 'etc', 'doge',
            'xlm', 'bch', 'xrp', 'trx', 'eos'
        ]
        self.dst_currencies = ['usdt', 'rls']
        if not self.token:
            self.token = self.login(username="mohammad.rafiei69@gmail.com", password="ZEmX7WHZxdVmmfY")
        self.headers = {"Authorization": f"Token {self.token}", "content-type": "application/json"}

    def call_api(self, path: str, data: dict=None, headers: dict=None):
        url = f'{self.base_url}{path}'
        response = requests.post(url, data=data, headers=headers)
        result = response.json()
        return result

    def login(self, username: str, password: str):
        data = {
            "username": username,
            "password": password,
            "captcha": "api",
            "remember": "yes"
        }
        response = self.call_api('/auth/login/', data)
        token = ''
        if response['status'] == 'success':
            token = response['key']
        return token

    def add_order(self, order: Order):
        data = {
            "type": order.type,
            "execution": "limit",
            "srcCurrency": order.src_currency,
            "dstCurrency": order.dst_currency,
            "amount": str(order.amount),
            "price": order.price
        }
        response = self.call_api('/market/orders/add', json.dumps(data), self.headers)
        return response

    def get_wallets(self):
        response = self.call_api('/users/wallets/list', headers=self.headers)
        wallets = response['wallets']
        user_wallets = [wallet for wallet in wallets if wallet['rialBalance'] > 0]
        return user_wallets

    def get_current_prices(self, dst_currency: str='rls'):
        srcCurrency = ','.join(self.src_currencies)
        data = {
            "srcCurrency": srcCurrency,
            "dstCurrency": dst_currency
        }
        response = self.call_api('/market/stats', data)
        return response['stats']

    def get_orderbook(self, symbol):
        url = f'{self.base_url}/v2/orderbook/{symbol}'
        response = requests.get(url)
        result = response.json()
        return result

    def get_trades(self, symbol):
        url = f'{self.base_url}/v2/trades/{symbol}'
        response = requests.get(url)
        result = response.json()
        return result
