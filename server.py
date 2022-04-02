from flask import Flask, redirect, render_template, request, session
from pymongo import MongoClient
from nobitexexchange import NobitexExchange
from order import Notification, Order


app = Flask(__name__)
app.secret_key = b'_5#y3L"F2Q8z\n\xec]/'
client = MongoClient('localhost', 27017)
db = client.crypto_db

exchange = NobitexExchange()


@app.route('/wallets/')
def get_wallets():
    wallets = exchange.get_wallets()
    return render_template('wallets.html', wallets=wallets)


@app.route('/add-order', methods=["GET", "POST"])
def add_order():
    if request.method == "GET":
        result = session.pop('add-order-result', None)
        return render_template('add_order.html', result=result)
    else:
        order = Order(
            type=request.form.get('order_type'),
            amount=request.form.get('amount', type=float),
            price=request.form.get('price', type=float),
            condition=request.form.get('condition', ''),
            src_currency=request.form.get('src_currency'),
            dst_currency=request.form.get('dst_currency'),
        )
        db.orders.insert_one(order.to_dict())
        session['add-order-result'] = 'success'
        # result = exchange.add_order(order)
        return redirect('/add-order')


@app.route('/add-notification', methods=["GET", "POST"])
def add_notification():
    if request.method == "GET":
        result = session.pop('add-notif-result', None)
        return render_template('add_notification.html', result=result)
    else:
        notification = Notification(
            type=request.form.get('notif_type'),
            price=request.form.get('price', type=float),
            condition=request.form.get('condition', ''),
            currency=request.form.get('currency'),
        )

        db.notifications.insert_one(notification.to_dict())
        session['add-notif-result'] = 'success'
        return redirect('/add-notification')


@app.route('/orderbook/')
def orderbook():
    stats = exchange.get_current_prices(dst_currency='usdt')
    print(stats['etc-usdt'])
    orders = exchange.get_orderbook('ETCUSDT')
    return render_template('orderbook.html', currency="ETC", orders=orders)
