import pymongo
from bson import ObjectId
from time import sleep
from nobitexexchange import NobitexExchange
from order import Notification, Order


client = pymongo.MongoClient('localhost', 27017)
db = client.crypto_db
exchange = NobitexExchange()


def main():
    while True:
        print('getting orders..')
        try:
            orderbook = exchange.get_orderbook('all')
            orderbook.pop('status')
            for doc in get_pending_orders():
                order = Order(**doc)
                symbol = (order.src_currency + order.dst_currency).upper()
                highest_ask = float(orderbook[symbol]['asks'][0][0])
                lowest_bid = float(orderbook[symbol]['bids'][0][0])
                print(symbol)
                if order.type == 'sell' and order.condition == 'up':
                    if order.price < highest_ask:
                        change_order_status(order._id, 'done')
                        print('#####', order)
                elif order.type == 'sell' and order.condition == 'down':
                    if order.price > lowest_bid:
                        change_order_status(order._id, 'done')
                        print('@@@@@', order)
                elif order.type == 'buy' and order.condition == 'up':
                    if order.price < highest_ask:
                        change_order_status(order._id, 'done')
                        print('$$$$$', order)
                elif order.type == 'buy' and order.condition == 'down':
                    if order.price > lowest_bid:
                        change_order_status(order._id, 'done')
                        print('*****', order)
        except:
            continue
        finally:
            sleep(10)


def get_pending_orders():
    orders = db.orders.find({'status': 'done'}).sort('created_at', pymongo.DESCENDING)
    return orders


def change_order_status(order_id, new_status):
    db.orders.update_one({'_id': order_id}, {'$set': {'status': new_status}})


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
