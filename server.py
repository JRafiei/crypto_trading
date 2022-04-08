from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for
from pymongo import MongoClient
from forms import OrderForm
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
    form = OrderForm()
    form.src_currency.choices = [(c, c.upper()) for c in exchange.src_currencies]
    form.dst_currency.choices = [(c, c.upper()) for c in exchange.dst_currencies]
    if form.validate_on_submit():
        order = Order(
            type=form.data.get('order_type'),
            amount=form.data.get('amount'),
            price=form.data.get('price'),
            condition=form.data.get('condition'),
            created_at=datetime.now(),
            src_currency=form.data.get('src_currency'),
            dst_currency=form.data.get('dst_currency'),
        )
        db.orders.insert_one(order.to_dict())
        session['add-order-result'] = 'success'
        # result = exchange.add_order(order)
        return redirect(url_for('add_order'))

    result = session.pop('add-order-result', None)
    return render_template('add_order.html', form=form, result=result)


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
