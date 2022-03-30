from flask import Flask, render_template, request
from nobitexexchange import NobitexExchange
from order import Order


app = Flask(__name__)


exchange = NobitexExchange()


@app.route('/wallets/')
def get_wallets():
    wallets = exchange.get_wallets()
    print(wallets)
    return render_template('wallets.html', wallets=wallets)


@app.route('/add-order', methods=["GET", "POST"])
def add_order():
    if request.method == "GET":
        return render_template('add_order.html')
    else:
        order = Order(
            type=request.form.get('order_type'),
            amount=request.form.get('amount'),
            price=request.form.get('price'),
            src_currency=request.form.get('src_currency'),
            dst_currency=request.form.get('dst_currency'),
        )

        result = exchange.add_order(order)
        return render_template('add_order.html', result=result)


@app.route('/orderbook/')
def orderbook():
    stats = exchange.get_current_prices(dst_currency='usdt')
    print(stats['etc-usdt'])
    orders = exchange.get_orderbook('ETCUSDT')
    return render_template('orderbook.html', currency="ETC", orders=orders)
