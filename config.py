from pydantic import BaseModel, BaseSettings


class DB(BaseModel):
    host = "139.162.11.227"
    port = 3306
    unix_socket = "/var/run/mysqld/mysqld.sock"
    user = "root"
    password = "ikok1987"
    db = 'shop'
    charset = "utf8"


class LINE(BaseModel):
    Channel_access_token = 'J74lonB5NIHXKVQ8bDX+0gE7rAonkcRc96aDbJpd3YNlMWy3cLB6DGVuVg7PXEOyWzECp/2jeMY2B70oxL0RiFIFc9prrlkUvQqnrHcfRcHOdy+jxxFu2OhNRXeF96Ucbe7VTJOGEvLSDpilVP3ijAdB04t89/1O/w1cDnyilFU='
    Channel_secret = 'cb22d7038aaaf85f014e311eb62b18da'
    User_id = 'Ub2b8849b4fd349622259537eb21f6b8c'


class EMAIL(BaseModel):
    sender = 'befreeberich0328@gmail.com'
    sender_token = 'hzgugcmkfutstaor'


class SMS(BaseModel):
    username = 'sjp4fu6'
    password = 'ikok1987'


class PAYMENT(BaseModel):
    official = {

    }
    test = {
        'MerchantID': '3002607',
        'HashKey': 'pwFHCqoQZGmho4w6',
        'HashIV': 'EkRm7iFT261dpevs',
        'action_url': 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
    }
    exec = test


class LOGISTIC(BaseModel):
    official = {

    }
    test = {
        'MerchantID': '2000933',
        'HashKey': 'XBERn1YOvpM9nfZc',
        'HashIV': 'h1ONHk4P4yqbl5LK',
        'action_url': 'https://logistics-stage.ecpay.com.tw/Express/',
        'search_action_url': 'https://logistics-stage.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V2',
        'print_action_url': 'https://logistics-stage.ecpay.com.tw/helper/printTradeDocument'
    }

    exec = test


class Settings(BaseSettings):
    #   APP 設定
    app_name: str = "SHOP API"
    admin_email: str = "sjp4fu6@gmail.com"
    #   DB 設定
    DB: DB = DB()
    #   EMAIL設定
    EMAIL: EMAIL = EMAIL()
    #   SMS 設定
    SMS: SMS = SMS()
    #   LINE 設定
    LINE: LINE = LINE()
    #   PAYMENT 設定
    PAYMENT: PAYMENT = PAYMENT()
    #   LOGISTIC 設定
    LOGISTIC: LOGISTIC = LOGISTIC()
    #   upload 設定
    UPLOAD_FOLDER: str = './upload/'  # '/var/www/upload'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'html', 'json'}
    ALLOWED_EXTENSIONS_MIME_TYPES = {"image/webp", "image/jpg", "image/jpeg", "image/png", "text/html", "text/json"}
    MAX_UPLOAD_SIZE = 100_000_000  # ~0MB

settings = Settings()
