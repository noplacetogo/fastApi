from pydantic import BaseModel, BaseSettings


class DB(BaseModel):
    host = "192.46.224.179"
    port = 3306
    unix_socket = "/var/run/mysqld/mysqld.sock"
    user = "root"
    password = "ikok1987"
    db = 'shop'
    charset = "utf8"


class EMAIL(BaseModel):
    sender = 'befreeberich0328@gmail.com'
    sender_token = 'hzgugcmkfutstaor'


class SMS(BaseModel):
    username = 'sjp4fu6'
    password = 'ikok1987'

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
    #   upload 設定
    UPLOAD_FOLDER: str = './upload/'  # '/var/www/upload'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'html', 'json'}
    ALLOWED_EXTENSIONS_MIME_TYPES = {"image/webp", "image/jpg", "image/jpeg", "image/png", "text/html", "text/json"}
    MAX_UPLOAD_SIZE = 100_000_000  # ~0MB

settings = Settings()
