import requests
import random
from responses import _recorder
from modules.TOOLS import get_token
from urllib.parse import urlencode
import os
base_url = "http://127.0.0.1:8000/"


class API:
    def __init__(self):
        self.url = base_url + 'api/'
        self.list = {
            'product_type': {
                'type_token': get_token('TYPE'),
                'type_name': random.choice(['二手書籍', '體育運品', '健身用具'])
            },
            'product': {
                'product_number': get_token('NO'),
                'type_token': get_token('TYPE'),
                'product_photo': 'https://upload.lovesusu.tw/IMG20200429001230.webp',
                'product_name': '六六狗肉',
                'sub_product_name': '狗頭:狗腿',
                'product_price': '100:150',
                'product_quantity': '10:5',
                'product_status': 2,
                'product_describe': '便宜好吃得狗肉',
            }
        }

    def get(self, table, data =None):
        if not data:
            return requests.get(self.url + f'{table}')
        else:
            return requests.get(self.url + f'{table}?' + urlencode(data))

    def post(self, table, data):
        return requests.post(self.url + f'{table}', json=data)


class UPLOAD:
    def __init__(self):
        self.url = base_url + 'upload/'

    def get(self):
        return requests.get(self.url)


class EMAIL:
    def __init__(self):
        self.page = base_url + 'email/sjp4fu6@gmail.com'

    def post(self):
        return requests.post(self.page, json={'subject': '測試郵件', 'detail': '郵件內容'})


class SMS:
    def __init__(self):
        self.page = base_url + 'sms/0978233315'

    def post(self):
        return requests.post(self.page, json={'detail': '測試電話中...'})


class LINE:
    # LINE 必須行駛於SSL上
    def __init__(self, _base_url=base_url):
        self.page = _base_url + 'line/'

    def broadcast(self, send_type='MSG', msg={'MSG': '測試中'}):
        return requests.post(f'{self.page}broadcast/{send_type}', json=msg)

    def push_message(self, user_id='Ub2b8849b4fd349622259537eb21f6b8c', send_type='MSG', msg={'MSG': '測試中'}):
        return requests.post(f'{self.page}pushMessage/{user_id}/{send_type}', json=msg)


class PAYMENT:
    def __init__(self):
        self.page = base_url + 'payment/'

    def to_ecpay(self):
        return requests.get(self.page + 'to_ecpay_test')


class LOGISTIC:
    def __init__(self):
        self.page = base_url + 'logistic/'
        self.order_ship = {
            'MerchantTradeNo': get_token("NO"),
            'MerchantTradeDate': "2022/11/16 16:00:00",
            'LogisticsSubType': "FAMILY_C2C",
            'TradeAmt': 1000,
            'order_product': "測試產品",
            'SenderName': "黃昱翊",
            'SenderPhone': "0978233315",
            'ReceiverName': "蘇東坡",
            'ReceiverPhone': "0978414414",
            'ReceiverEmail': "sjp4fu6@gmail.com",
            'TradeDesc': "測試產品100元*1#測試產品200元*2",
            "ReceiverStoreID": "006598",
            "ReturnStoreID": "006598"
        }
        self.logistic_id = '2088697'

    def map_test(self):
        return requests.get(self.page + 'map_test')
    
    def create_shipping_order_c2c(self):
        token = get_token("NO")
        self.order_ship['MerchantTradeNo'] = token
        return requests.post(f'{self.page}create_shipping_order_C2C/{token}', json=self.order_ship)

    def search_shipping_order_c2c(self):
        return requests.get(f'{self.page}search_shipping_order_C2C/{ self.logistic_id}')

@_recorder.record(file_path="out.toml")
def main():
    # print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    # # 測試API
    # api = API()
    # for i in [api.get(i) for i in api.list.keys()]:
    #     assert i.status_code == 200
    # for i in [api.get(i, api.list[i]) for i in api.list.keys()]:
    #     assert i.status_code == 200
    # for i in [api.post(i, api.list[i]) for i in api.list.keys()]:
    #     assert i.status_code == 200
    #
    # # 測試upload
    # upload = UPLOAD()
    # assert upload.get().status_code == 200
    #
    # # 測試email
    # email = EMAIL()
    # assert email.post().status_code == 200
    #
    # # 測試sms
    # sms = SMS()
    # assert sms.post().status_code == 200
    #
    # # 測試LINE
    # line = LINE()
    # assert line.broadcast().status_code == 200
    # assert line.push_message().status_code == 200
    #
    # # 測試payment
    # payment = PAYMENT()
    # assert payment.to_ecpay().status_code == 200

    # 測試logistic
    logistic = LOGISTIC()
    # assert logistic.map_test().status_code == 200
    # assert logistic.create_shipping_order_c2c().status_code == 200
    # assert logistic.search_shipping_order_c2c().status_code == 200

    return None

main()

