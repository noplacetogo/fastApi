import sys
import requests
import urllib.parse
from config import settings
sys.path.append('..')


class SMS:
    @classmethod
    def send(cls, receiver_phone: str = '0978233315', content: str = '測試內容',
                params: dict = {'username': settings.SMS.username, 'password': settings.SMS.password}):
        try:
            url_twsms = 'https://api.twsms.com/json/sms_send.php?username={}&password={}&mobile={}&message={}' \
                .format(params['username'], params['password'],
                        receiver_phone, urllib.parse.quote_plus(content))
            res = requests.get(url_twsms)
            return res.json()
        except Exception as e:
            print("Error message: ", e)
