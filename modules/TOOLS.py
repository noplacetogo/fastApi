import uuid
import hashlib
from fastapi import Request, HTTPException, Depends, Header
from urllib.parse import quote_plus
from config import settings
import html
import uuid
import requests
from datetime import datetime
import collections
import re


def dict_protect_sql(params: dict) -> dict:
    regex = "(^[A-Za-z0-9_@]+$)"
    params_ = {}
    for key, values in params.items():
        params_[key] = str(html.escape(values.replace("'", '"').replace("-", '_').replace(";", ':')))
        if len(re.findall(regex, key)) == 0:
            raise HTTPException(status_code=401, detail='參數錯誤!')
        if key == values:
            raise HTTPException(status_code=401, detail='參數錯誤!')
      # elif len(re.findall(regex, str(values))) == 0:
      #    print('參數錯誤')
      #    raise HTTPException(status_code=401, detail='參數錯誤!')
    return params_


# dict ->dict
def parse_params_to_sql(params: dict) -> str:
    params = dict_protect_sql(params)
    return "&".join([f"{i}='{params[i]}'" for i in params])


# create uuid
def getUUID() -> str:
    temp = str(uuid.uuid4())
    return temp.replace('-', '')


# 驗證綠界傳送的 check_mac_value 值是否正確
def get_mac_value(get_request_form) -> str:
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


def get_token(prefix='') -> str:
  temp = str(uuid.uuid4())
  token = temp.replace('-', '')
  now = datetime.now()
  nowStr = now.strftime('%y%m%d%H%M%S')
  restNumber = 20 - (len(prefix) + len(nowStr))
  return prefix + now.strftime('%y%m%d%H%M%S') + token[0:restNumber]


async def payload_(request: Request) -> dict:
    _payload = {}
    try:
        _payload = dict(await request.form())
        _payload.update(await request.json())
    except Exception as e:
        pass
    return dict_protect_sql(_payload)


async def google_recaptcha(request: Request, gr: str = Header()):
    if gr == '':
        raise HTTPException(status_code=401, detail="gr token invaild")
    token = gr
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
            return payload_(request)
        else:
            raise HTTPException(status_code=401, detail='gr token bot')



