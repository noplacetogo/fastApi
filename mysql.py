import pymysql
import collections
import aiomysql

class SQL:
  @classmethod
  async def connect(cls):
    db_settings = {
#         "host": "192.46.224.179",
#         "port": 3306,
        "unix_socket": "/var/run/mysqld/mysqld.sock",
        "user": "root",
        "password": "ikok1987",
        "db": 'shop',
        "charset": "utf8",
    }
    return await aiomysql.create_pool(**db_settings)
  
  # Rapid API 
  # get,update,delete
  @classmethod
  async def get(cls, pool, table):
    columns = DB.getColumns(table)
    queryStr = "SELECT * FROM {}".format(table)
    res = collections.deque(list(await cls().querySQL(pool, queryStr, 'select')))
    res.appendleft(columns)
    return list(res)

  @classmethod
  async def update(cls, table, *argv):
    queryKey = ','.join(list(argv[0].keys()))
    queryValue = ','.join(["'{}'".format(i) for i in list(argv[0].values())])
    querySet = ','.join(["{}='{}'".format(i[0], i[1]) for i in list(argv[0].items())])
    queryStr = "INSERT INTO {} ({}) VALUES ({}) on DUPLICATE KEY UPDATE {};".format(table, queryKey, queryValue, querySet)
    await cls().querySQL(pool, queryStr, 'shop', 'commit')

  @classmethod
  async def delete(cls, table, *argv):
    self.conn.ping()
    queryWhere = "{}='{}'".format(*list(argv[0].items())[0])
    queryStr = "DELETE FROM {} WHERE {} ".format(table, queryWhere)
    await cls().querySQL(pool, queryStr, 'shop', 'commit')

  # Complex API
  # search
  @classmethod
  async def query(self, table, command):
    columns = tuple(command.split('SELECT')[1].split('FROM')[0].replace(' ','').split(','))
    res = collections.deque(list(await cls().querySQL(pool, command, 'select')))
    res.appendleft(columns)
    return list(res)  
      


  async def querySQL(self, pool, command, type='commit'):
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute(command)
        if type == 'commit':
          conn.commit()
        else:
          return await cur.fetchall()

class DB:
    def __init__(self):
        self.table = {
            'product_type': {
                'table_name': 'product_type',
                'type_token': 'VARCHAR(32)',
                'type_name': 'VARCHAR(32)',
            },
            'product': {
                'table_name': 'product',
                'id': 'int auto_increment primary key',
                'product_number': 'VARCHAR(20)',
                'type_token': 'VARCHAR(32)',
                'product_photo': 'VARCHAR(320)',
                'product_name': 'VARCHAR(150)',
                'sub_product_name': 'VARCHAR(150)',
                'product_price': 'VARCHAR(150)',
                'product_quantity': 'VARCHAR(150)',
                'product_status': 'INT(1)',
                'product_describe': 'VARCHAR(150)',
                'market_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'update_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            },
            'product_detail': {
                'table_name': 'product_detail',
                'id': 'int auto_increment primary key',
                'product_number': 'VARCHAR(20)',
                'product_describe_photo': 'TEXT',
                'product_describe_detail': 'TEXT',
                'product_specification': 'TEXT',
                'product_deliver': 'TEXT'
            },
            'order_info': {
                'table_name': 'order_info',
                'id': 'int auto_increment primary key',
                'order_token': 'VARCHAR(32)',
                'order_number': 'VARCHAR(20)',
                'order_name': 'VARCHAR(30)',
                'order_phone': 'VARCHAR(10)',
                'order_product': 'VARCHAR(300)',
                'order_event_code': 'VARCHAR(100)',
                'order_price': 'INT(32)',
                'order_status': 'INT(1)',
                'order_comment': 'VARCHAR(200)',
                'payment_status': 'INT(1)',
                'store_info': 'VARCHAR(200)',
                'order_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'update_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            },
            'order_info_detail': {
                'table_name': 'order_info_detail',
                'id': 'int auto_increment primary key',
                'order_token': 'VARCHAR(32)',
                'order_number': 'VARCHAR(20)',
                'MerchantTradeNo': 'VARCHAR(20)',
                'StoreID': 'VARCHAR(20)',
                'card6no': 'INT(6)',
                'card4no': 'INT(4)',
                'RtnCode': 'INT(1)',
                'RtnMsg': 'VARCHAR(200)',
                'TradeNo': 'VARCHAR(20)',
                'TradeAmt': 'INT',
                'PaymentTypeChargeFee': 'INT',
                'PaymentDate': 'VARCHAR(20)',
                'PaymentType': 'VARCHAR(20)',
                'TradeDate': 'VARCHAR(20)',
                'payment_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            },
            'email': {
                'table_name': 'email',
                'id': 'int auto_increment primary key',
                'user_token': 'VARCHAR(32)',
                'user_id': 'VARCHAR(32)',
                'user_email': 'VARCHAR(320)',
                'email_permit': 'INT(1)',
            },
            'emailAccount': {
                'table_name': 'emailAccount',
                'id': 'int auto_increment primary key',
                'account_token': 'VARCHAR(32)',
                'account_name': 'VARCHAR(32)',
                'account_account': 'VARCHAR(320)',
                'account_password': 'VARCHAR(32)',
                'account_main': 'INT(1)'
            },
            'lineAccount': {
              'table_name': 'lineAccount',
              'id': 'int auto_increment primary key',
              'account_token': 'VARCHAR(32)',
              'account_name': 'VARCHAR(32)',
              'Channel_access_token': 'VARCHAR(320)',
              'Channel_secret': 'VARCHAR(64)',
              'User_id': 'VARCHAR(64)',
              'account_main': 'INT(1)' 
            },
            'message': {
                'table_name': 'message',
                'id': 'int auto_increment primary key',
                'message_token': 'VARCHAR(32)',
                'message_name': 'VARCHAR(64)',
                'message_content': 'TEXT',
                'message_url': 'TEXT',
                'message_comment': 'TEXT',   
            },
            'reserve': {
                'table_name': 'reserve',
                'id': 'int auto_increment primary key',
                'reserve_token': 'VARCHAR(32)',
                'reserve_send_method': 'VARCHAR(32)',
                'reserve_sender': 'VARCHAR(320)',
                'reserve_title': 'VARCHAR(32)',
                'reserve_content': 'TEXT',
                'reserve_receiver': 'TEXT',
                'reserve_type':'VARCHAR(320)',
                'reserver_status': 'INT(1)',
                'reserve_send_time': 'VARCHAR(32)',
                'reserve_time': 'VARCHAR(32)'
            },
            'bot': {
                'table_name': 'bot',
                'id': 'int auto_increment primary key',
                'reply_token':'VARCHAR(32)',
                'reply_method':'VARCHAR(32)',
                'reply_type':'VARCHAR(32)',
                'reply_content':'TEXT',
                'reply_status':'INT(1)'
            },
            'member': {
                'table_name': 'member',
                'id': 'int auto_increment primary key',
                'user_token': 'VARCHAR(32)',
                'user_id': 'VARCHAR(32)',
                'line_id': 'VARCHAR(64)',
                'google_id': 'VARCHAR(32)',
                'fb_id': 'VARCHAR(32)',
                'user_email': 'VARCHAR(320)',
                'user_phone': 'VARCHAR(10)',
                'user_account': 'VARCHAR(32)',
                'user_password': 'VARCHAR(32)',
                'user_verify': 'VARCHAR(32)',
                'user_status': 'INT(1)',
                'temp_login': 'INT(6)',
                'reg_date': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'login_date': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            },
            'member_token': {
                'table_name': 'member_token',
                'id': 'int auto_increment primary key',
                'user_id': 'VARCHAR(32)',
                'authToken': 'VARCHAR(32)',
                'status': 'INT(1)',
                'iat': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'ip': 'VARCHAR(16)',
            },
            'member_detail': {
                'table_name': 'member_detail',
                'id': 'int auto_increment primary key',
                'user_id': 'VARCHAR(32)',
                'user_name': 'VARCHAR(32)',
                'user_address': 'VARCHAR(256)',
                'user_gender': 'VARCHAR(4)',
                'user_level': 'VARCHAR(32)',
                'user_comment': 'TEXT',
            },

            'staff': {
                'table_name': 'staff',
                'id': 'int auto_increment primary key',
                'user_token': 'VARCHAR(32)',
                'user_id': 'VARCHAR(32)',
                'user_account': 'VARCHAR(32)',
                'user_password': 'VARCHAR(32)',
                'user_status': 'INT(1)',
                'temp_login': 'INT(6)',
                'reg_date': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'login_date': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            },
            'staff_token': {
                'table_name': 'staff_token',
                'id': 'int auto_increment primary key',
                'user_id': 'VARCHAR(32)',
                'authToken': 'VARCHAR(32)',
                'status': 'INT(1)',
                'iat': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'ip': 'VARCHAR(16)',
            },
            'staff_detail': {
                'table_name': 'staff_detail',
                'id': 'int auto_increment primary key',
                'user_id': 'VARCHAR(32)',
                'user_number': 'VARCHAR(4)',
                'user_name': 'VARCHAR(32)',
                'user_position': 'VARCHAR(32)',
                'user_permission': 'VARCHAR(128)',
                'user_comment': 'VARCHAR(256)'
            },
            'staff_record': {
                'table_name': 'staff_record',
                'id': 'int auto_increment primary key',
                'user_id': 'VARCHAR(32)',
                'record_type': 'VARCHAR(16)',
                'record_content': 'VARCHAR(256)',
                'record_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            },
            'event': {
                'table_name': 'event',
                'event_token': 'varchar(32)',
                'event_status': 'INT',
                'event_order': 'INT',
                'event_name': 'varchar(32)',
                'event_start': 'DATE',
                'event_end': 'DATE',
                'event_photo': 'TEXT',
                'event_describe': 'TEXT',
                'event_method': 'TEXT'
            },
            'article': {
                'table_name': 'article',
                'id': 'int auto_increment primary key',
                'article_token': 'VARCHAR(32)',
                'article_photo': 'VARCHAR(150)',
                'article_title': 'VARCHAR(150)',
                'article_author': 'VARCHAR(150)',
                'article_tag': 'VARCHAR(150)',
                'article_status': 'INT(1)',
                'article_outline': 'VARCHAR(150)',
                'update_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            },
            'article_detail': {
                'table_name': 'article_detail',
                'id': 'int auto_increment primary key',
                'article_token': 'VARCHAR(32)',
                'article_content': 'TEXT',

            },
            'chat_group': {
                'table_name': 'chat_group',
                'id': 'int auto_increment primary key',
                'group_token': 'VARCHAR(32)',
                'group_id': 'VARCHAR(32)',
                'group_status': 'INT(1)', #0,1 public,private 
                'user_id': 'VARCHAR(32)',
            },
            'chat_message': {
                'table_name': 'chat_message',
                'id': 'int auto_increment primary key',
                'chat_token': 'VARCHAR(32)',
                'group_id': 'VARCHAR(32)',
                'user_id': 'VARCHAR(32)',
                'chat_content': 'TEXT',
                'update_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            },


        }

    @classmethod
    def getTableList(cls):
        res = {i: list(cls().table[i].keys())[1:] for i in cls().table}
        return res

    @classmethod
    def getColumns(cls, table_name):
      table = cls().table[table_name]
      return tuple(list(table.keys())[2:])
    @classmethod
    def truncate(cls, table):
        query = "TRUNCATE TABLE {} ".format(table)
        cls().querySQL(query, 'shop', 'commit')

    @classmethod
    def drop(cls, table):
        query = "DROP TABLE {} ".format(table)
        print(query)
        cls().querySQL(query, 'shop', 'commit')

    @classmethod
    def create(cls, table_name):
        table = cls().table[table_name]
        table_setting = ','.join([' '.join(i) for i in list(table.items())[1:]])
        query = 'create table {} ( {} );'.format(list(table.values())[0], table_setting)
        print(query)
        cls().querySQL(query, 'shop', 'commit')

    @classmethod
    def get(cls):
      query = 'SELECT * FROM product'
      return cls().querySQL(query,'shop','search')
      
    def querySQL(self, query, database, type='commit'):
        global conn
        # 資料庫設定
        db_settings = {
            "host": "192.46.224.179",
            "port": 3306,
            "user": "root",
            "password": "ikok1987",
            "db": database,
            "charset": "utf8"
        }
        try:
            # 建立Connection物件
            conn = pymysql.connect(**db_settings)
        except Exception as ex:
            print(ex)
        with conn.cursor() as cursor:
            # 新增資料指令
            command = query
            # 執行指令
            cursor.execute(command)
            if type == 'commit':
                conn.commit()
                cursor.close()
                conn.close()
            else:
                # 取得前五筆資料
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
