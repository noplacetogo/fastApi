import re
from modules.CRUD import SQL


def dispatch_work(work, event, query_gex):
  if work == '註冊':
    if len(query_gex) == 0:
      return '如要註冊請輸入電話或信箱'
    print(event, query_gex[0][0], query_gex[0][1])
    return '註冊成功'
  elif work == '登入':
    print(work, query_gex)
  elif work == '查詢訂單':
    if len(query_gex) == 0:
      # 查詢無註冊
      print('查詢有無註冊')
      member = ['']
      if len(member) == 0:
        return '如要查詢訂單請先行註冊。\n輸入範例：註冊 0978******'
      # 查詢有註冊，查詢尚未完成訂單
      print('查詢尚未完成訂單')
      order_info = ['']
      if len(order_info) == 0:
        return '無訂單資訊!'
      order_info_ = []
      for i in order_info:
        order_info_.append({
          'order_number': i[0],
          'order_name': i[1],
          'order_phone': query_gex[0][1],
          'order_product': i[2],
          'order_event_code': i[3],
          'order_price': i[4],
          'order_status': i[5],
          'store_info': i[6],
          'order_time': i[7],
          })
      for i in order_info_:
        print('依照訂單，回應訂單資訊')
        return "查詢中請稍後"
    else:
      # 未註冊查詢
      # 此部分需修改 bot.BOT.botReply 因該函式需透過電話查詢會員註冊取得lineID
      return '不懂你的意思'

# 處理LINE對話
def robot(event):
  mark_list = ['註冊', '登入', '查詢訂單']
  regex = [('電話', '(?<!\d)\d{10}(?!\d)'),
                ('郵箱', "([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"),
                ('訂單編號', '(^NO)[A-Za-z0-9]{13}(?![A-Za-z0-9])')]
  query = event.message.text.strip()
  if len(query) == 0:
    return "不懂您的意思!"
  query_res = [i for i in mark_list if i in query]
  query_gex = [(i[0], re.findall(i[1], query)[0]) for i in regex if len(re.findall(i[1], query)) != 0]
  for i in query_res:
    return event.reply_token, dispatch_work(i, event, query_gex)
