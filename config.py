from pydantic import BaseModel, BaseSettings

class DB(BaseModel):
#         "host" = "192.46.224.179"
#         "port" = 3306
        unix_socket = "/var/run/mysqld/mysqld.sock"
        user = "root"
        password = "ikok1987"
        db = 'shop'
        charset = "utf8"

class Settings(BaseSettings):
#   APP 設定
    app_name: str = "SHOP API"
    admin_email: str = "sjp4fu6@gmail.com"
#   DB 設定
    DB: DB = DB()


settings = Settings()
