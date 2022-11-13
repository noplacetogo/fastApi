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
    def __init__(self):
        self.page = base_url + 'line/'

    def broadcast(self, send_type='MSG', msg={'MSG': '測試中'}):
        return requests.post(f'{self.page}broadcast/{send_type}', json=msg)

    def push_message(self, user_id='Ub2b8849b4fd349622259537eb21f6b8c', send_type='MSG', msg={'MSG': '測試中'}):
        return requests.post(f'{self.page}broadcast/{user_id}/{send_type}', json=msg)
@_recorder.record(file_path="out.toml")
def main():
    # print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    # 測試API
    # api = API()
    # for i in [api.get(i) for i in api.list.keys()]:
    #     assert i.status_code == 200
    # for i in [api.get(i, api.list[i]) for i in api.list.keys()]:
    #     assert i.status_code == 200
    # for i in [api.post(i, api.list[i]) for i in api.list.keys()]:
    #     assert i.status_code == 200

    # 測試upload
    # upload = UPLOAD()
    # assert upload.get().status_code == 200

    # 測試email
    # email = EMAIL()
    # assert email.post().status_code == 200

    # 測試sms
    # sms = SMS()
    # assert  sms.post().status_code == 200

    # 測試LINE
    # line = LINE()
    # assert line.broadcast().status_code == 200
    # assert line.push_message().status_code == 200
    return None

main()