from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import  List, Union
from modules.CRUD import SQL
from modules.TOOLS import parse_params_to_sql, get_token, get_mac_value, payload_
from config import settings
import importlib.util
import time
import os
import sys

filename = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk", filename + "/sdk/ecpay_logistic_sdk.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.path.append('..')

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/map', tags=['LOGISTIC'], summary="重定向綠界地圖")
async def map(payload: dict = Depends(payload_)):
    """
    :param payload:['subType','returnUrl','frontUrl','device']
    :return: html
    """
    cvs_map_params = {
        "MerchantTradeNo": "anyno",
        "LogisticsType": "CVS",
        # 若申請類型為 B2C，只能串參數為 FAMI、UNIMART、HILIFE
        # 若申請類型為 C2C，只能串參數為 FAMIC2C、UNIMARTC2C、HILIFEC2C
        "LogisticsSubType": payload['subType'],
        "IsCollection": "N",
        # "ServerReplyURL": host_name + "logistic/map_result",
        "ServerReplyURL": payload['returnUrl'],
        "ExtraData": payload['frontUrl'],
        "Device": module.Device[payload['device']],
    }

    # 建立實體
    ecpay_logistic_sdk = module.ECPayLogisticSdk(
        MerchantID=settings.LOGISTIC.dict()['exec']['MerchantID'],
        HashKey=settings.LOGISTIC.dict()['exec']['HashKey'],
        HashIV=settings.LOGISTIC.dict()['exec']['HashIV']
    )
    try:
        # 產生綠界物流訂單所需參數
        final_params = ecpay_logistic_sdk.cvs_map(cvs_map_params)
        html = ecpay_logistic_sdk.gen_html_post_form(settings.LOGISTIC.dict()['exec']['action_url'], final_params)
        return html
    except Exception as error:
        print('An exception happened: ' + str(error))


@router.post('/map_result', tags=['LOGISTIC'], summary="綠界地圖回傳")
async def map_result(payload: dict = Depends(payload_)):
    front_url = payload['ExtraData'] + '?' + 'CVSStoreID=' +\
                payload['CVSStoreID'] + '&CVSStoreName=' + payload['CVSStoreName'] +\
                '&CVSAddress=' + payload['CVSAddress']
    return RedirectResponse(front_url)


@router.post("/create_shipping_order_C2C/{MerchantTradeNo}", tags=['LOGISTIC'], summary="新增物流")
async def create_shipping_order_c2c(payload: dict = Depends(payload_)):
    create_shipping_order_params = {
        'MerchantTradeNo': payload['MerchantTradeNo'],
        'MerchantTradeDate': payload['MerchantTradeDate'],
        'LogisticsType': module.LogisticsType['CVS'],
        'LogisticsSubType': module.LogisticsSubType[payload['LogisticsSubType']],
        'GoodsAmount': payload['TradeAmt'],
        'CollectionAmount': payload['TradeAmt'],
        'IsCollection': module.IsCollection['YES'],
        'GoodsName': payload['order_product'],
        'SenderName':  payload['SenderName'],
        'SenderPhone':  payload['SenderPhone'],
        'SenderCellPhone':  payload['SenderPhone'],
        'ReceiverName':  payload['ReceiverName'],
        'ReceiverPhone':  payload['ReceiverPhone'],
        'ReceiverCellPhone':  payload['ReceiverPhone'],
        'ReceiverEmail':  payload['ReceiverEmail'],
        'TradeDesc':  payload['TradeDesc'],
        'ServerReplyURL': 'https://lovesusu.tw/shop/api/logistic/receive_result',
        'ClientReplyURL': '',
        'Remark': '測試備註',
        'PlatformID': '',
        'LogisticsC2CReplyURL': 'https://www.ecpay.com.tw/logistics_c2c_reply',
    }
    shipping_cvs_params = {
        'ReceiverStoreID': payload['ReceiverStoreID'],
        'ReturnStoreID': payload['ReturnStoreID'],
    }
    create_shipping_order_params.update(shipping_cvs_params)
    ecpay_logistic_sdk = module.ECPayLogisticSdk(
        MerchantID=settings.LOGISTIC.dict()['exec']['MerchantID'],
        HashKey=settings.LOGISTIC.dict()['exec']['HashKey'],
        HashIV=settings.LOGISTIC.dict()['exec']['HashIV']
    )
    try:
        reply_result = ecpay_logistic_sdk.create_shipping_order(
            action_url=settings.LOGISTIC.dict()['exec']['action_url'],
            client_parameters=create_shipping_order_params)
        return reply_result
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)


@router.get("/search_shipping_order_C2C/{logistics_id}", tags=['LOGISTIC'], summary='取得物流')
async def search_shipping_order_c2c(logistics_id: str):
    query_logistics_info_params = {
        'AllPayLogisticsID': logistics_id,
        'TimeStamp': int(time.time()),
        'PlatformID': '',
    }
    ecpay_logistic_sdk = module.ECPayLogisticSdk(
        MerchantID=settings.LOGISTIC.dict()['exec']['MerchantID'],
        HashKey=settings.LOGISTIC.dict()['exec']['HashKey'],
        HashIV=settings.LOGISTIC.dict()['exec']['HashIV']
    )
    try:
        reply_result = ecpay_logistic_sdk.query_logistics_info(
            action_url=settings.LOGISTIC.dict()['exec']['action_url'],
            client_parameters=query_logistics_info_params)
        return reply_result
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)


@router.post('/receive_result', tags=['LOGISTIC'], summary="物流回傳資料")
async def receive_result(payload: dict = Depends(payload_)):
    print(payload)
    return '1|OK'


@router.get('/print_trade_doc/{logistics_id}', tags=['LOGISTIC'], summary="列印託運單")
def print_trade_doc(logistics_id: str):
    print_trade_doc_params = {
        'AllPayLogisticsID': logistics_id,
        'PlatformID': '',
        'ClientReplyURL': '',
    }
    # 建立實體
    ecpay_logistic_sdk = module.ECPayLogisticSdk(
        MerchantID=settings.LOGISTIC.dict()['exec']['MerchantID'],
        HashKey=settings.LOGISTIC.dict()['exec']['HashKey'],
        HashIV=settings.LOGISTIC.dict()['exec']['HashIV']
    )
    try:
        # 產生綠界物流訂單所需參數
        final_params = ecpay_logistic_sdk.print_trade_doc(
            client_parameters=print_trade_doc_params)
        html = ecpay_logistic_sdk.gen_html_post_form(
            action_url=settings.LOGISTIC.dict()['exec']['action_url'],
            client_parameters=final_params)
        return html
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)

