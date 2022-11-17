import uuid
import hashlib
from fastapi import Request, HTTPException
from urllib.parse import quote_plus
from config import  settings
import uuid
from datetime import datetime
import collections


# dict ->dict
# {"apple":"3" => apple='3'}
def parse_params_to_sql(params: dict) -> str:
    return "&".join([f"{i}='{params[i]}'" for i in params])


# create uuid
def getUUID() -> str:
    temp = str(uuid.uuid4())
    return temp.replace('-', '')


# 驗證綠界傳送的 check_mac_value 值是否正確
def get_mac_value(get_request_form):
    params = dict(get_request_form)
    if params.get('CheckMacValue'):
        params.pop('CheckMacValue')
    ordered_params = collections.OrderedDict(
        sorted(params.items(), key=lambda k: k[0].lower()))
    HahKy = settings.PAYMENT.dict()['exec']['HashKey']
    HashIV = settings.PAYMENT.dict()['exec']['HashIV']
    encoding_lst = []
    encoding_lst.append('HashKey=%s&' % HahKy)
    encoding_lst.append(''.join([
        '{}={}&'.format(key, value)
        for key, value in ordered_params.items()
    ]))
    encoding_lst.append('HashIV=%s' % HashIV)
    safe_characters = '-_.!*()'
    encoding_str = ''.join(encoding_lst)
    encoding_str = quote_plus(str(encoding_str),
                           safe=safe_characters).lower()
    check_mac_value = hashlib.sha256(
        encoding_str.encode('utf-8')).hexdigest().upper()
    return check_mac_value


def get_token(prefix=''):
  temp = str(uuid.uuid4())
  token = temp.replace('-', '')
  now = datetime.now()
  nowStr = now.strftime('%y%m%d%H%M%S')
  restNumber = 20 - (len(prefix) + len(nowStr))
  return prefix + now.strftime('%y%m%d%H%M%S') + token[0:restNumber]


async def payload_(request: Request):
    _payload = {}
    try:
        _payload = dict(await request.form())
        _payload.update(await request.json())
    except Exception as e:
        pass
    return _payload

async def googleRecaptcha(payload: dict = Depands(payload_))
    token = payload.get('gr','')
    if token == '':
        raise HTTPException(status_code=401, detail='gr token ERROR')
    googleUrl = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': '6LcxdFEiAAAAAHUHnSVZBN9crhGWiL0McbCZjIYC',
        'response': token,
    }
    r = requests.post(googleUrl, data)
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail='gr token request Error')
    with r.json() as res:
        if res.score >= 0.5:
            payload.pop('gr')
            return payload
        else:
            raise HTTPException(status_code=401, detail='gr token bot')

