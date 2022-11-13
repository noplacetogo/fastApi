from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import  List, Union
from modules.CRUD import SQL
from modules.TOOLS import parse_params_to_sql, get_token
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


@router.get("/", response_class=HTMLResponse, tags=['PAYMENT'])
async def index(request: Request):
    return templates.TemplateResponse("dealPage.html", {"request": request})


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
    ecpay_payment_sdk = module.ECPayPaymentSdk(MerchantID=settings.PAYMENT.exec.dict()['MerchantID'],
                                               HashKey=settings.PAYMENT.exec.dict()['HashKey'],
                                               HashIV=settings.PAYMENT.exec.dict()['HashIV'])
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = settings.PAYMENT.exec.dict()['action_url']
        html = ecpay_payment_sdk.gen_html_post_form(action_url,
                                                    final_order_params)
        return html
    except Exception as error:
        print('An exception happened: ' + str(error))


@router.post('/to_ecpay_test', response_class=HTMLResponse, tags=['PAYMENT'])
async def to_ecpay_text(request: Request):
    return to_ecpay()

