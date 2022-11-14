from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import  List, Union
from modules.CRUD import SQL
from modules.TOOLS import parse_params_to_sql, get_token, get_mac_value, payload_
from config import settings
import importlib.util
import os
import sys

filename = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", filename + "/sdk/ecpay_payment_sdk.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.path.append('..')

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def to_ecpay(cart=None):
    # 處理基本資料
    # total_product_price = [i['price']*i['quantity'] for i in carts]
    # total_product_name = [f"{i['product_name']}{str(i['price'])}元x{str(i['quantity'])}" for i in carts]
    if cart is None:
        cart = {'total_product_price': 100,
                'total_product_name': '測試商品100元x1',
                'order_number': get_token('NO'),
                'order_phone': '0978233315',
                'order_name': '康熙來了',
                'order_time': '2022/06/12 12:00:00'
                }
    host_name = "https://lovesusu.tw/shop/"

    order_params = {
        'MerchantTradeNo':  cart['order_number'],
        'StoreID': '',
        'MerchantTradeDate': cart['order_time'],
        'PaymentType': 'aio',
        'TotalAmount': cart['total_product_price'],
        'TradeDesc': 'ToolsFactory',
        'ItemName': cart['total_product_name'],
        'ReturnURL': host_name + 'payment/receive_result',
        'ChoosePayment': 'Credit',
        'ClientBackURL': host_name + 'payment/trad_result',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': host_name + 'payment/trad_result',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': cart['order_phone'],
        'CustomField2': cart['total_product_name'],
        'CustomField3': cart['order_name'],
        'CustomField4': '',
        'EncryptType': 1,
    }
    ecpay_payment_sdk = module.ECPayPaymentSdk(MerchantID=settings.PAYMENT.dict()['exec']['MerchantID'],
                                               HashKey=settings.PAYMENT.dict()['exec']['HashKey'],
                                               HashIV=settings.PAYMENT.dict()['exec']['HashIV'])
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = settings.PAYMENT.dict()['exec']['action_url']
        html = ecpay_payment_sdk.gen_html_post_form(action_url,
                                                    final_order_params)
        return html
    except Exception as error:
        print('An exception happened: ' + str(error))


@router.get('/to_ecpay_test', response_class=HTMLResponse, tags=['PAYMENT'], summary="測試金流")
async def to_ecpay_test(request: Request):
    return to_ecpay()


@router.post('/receive_result', tags=['PAYMENT'], summary="金流回傳資料")
async def receive_result(payload: dict = Depends(payload_)):
    """
    自綠界後台接收資訊
    :param payload:[]
    :return: html
    """
    print(payload)
    return '1|OK'


@router.post('/trad_result', tags=['PAYMENT'], summary="金流頁面重定向個人網頁")
async def trad_result(request: Request, payload: dict = Depends(payload_)):
    if get_mac_value(payload) != payload['CheckMacValue']:
        return '請聯繫管理員'
    return templates.TemplateResponse("trade_res.html", {"request": request})
