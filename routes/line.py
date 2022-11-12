import sys
from fastapi import APIRouter, Request,  HTTPException, BackgroundTasks
from config import settings
from reflects.ROBOT import robot
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.exceptions import LineBotApiError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,FlexSendMessage)
sys.path.append('..')
router = APIRouter()
# 初始化 LINE
line_bot_api = LineBotApi(settings.LINE.dict()['Channel_access_token'])
handler = WebhookHandler(settings.LINE.dict()['Channel_secret'])
default_user_id = settings.LINE.dict()['User_id']

# 測試 LINE CALLBACK
@router.post("/callback", tags=['LINE'])
async def _callback(request: Request):
  signature = request.headers["X-Line-Signature"]
  body = await request.body()
  # handle webhook body
  try:
    handler.handle(body.decode(), signature)
  except InvalidSignatureError:
    raise HTTPException(status_code=400, detail="Missing Parameter")
  return "OK"


# 機器人回應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  reply = robot(event)
  line_bot_api.reply_message(
            reply[0],
            TextSendMessage(text=reply[1]))


# 推播 BROADCAST
@router.post('/broadcast/{send_type}', tags=['LINE'])
async def broadcast(send_type: str, request: Request, background_tasks: BackgroundTasks):
  msg = await request.json()
  if send_type == "MSG":
    text_message = TextSendMessage(text=msg['MSG'])
    background_tasks.add_task(line_bot_api.broadcast, text_message)
  elif send_type == "IMG":
    image_message = ImageSendMessage(
      original_content_url=msg['IMG'],
      preview_image_url=msg['IMG']
    )
    background_tasks.add_task(line_bot_api.broadcast, image_message)
  else:
    flex_message = FlexSendMessage(alt_text='Flex Msg', contents=msg)
    background_tasks.add_task(line_bot_api.broadcast, flex_message)
  return {'def': "broadcast", "msg":msg}


# 推送 PUSH-MESSAGE
@router.post('/pushMessage/{user_id}/{send_type}', tags=['LINE'])
async def push_message(user_id: str,send_type: str, request: Request, background_tasks: BackgroundTasks):
  msg = await request.json()
  try:
    if send_type == 'MSG':
      text_message = TextSendMessage(text=msg['MSG'])
      background_tasks.add_task(line_bot_api.push_message, user_id, text_message)
    elif send_type == 'IMG':
      image_message = ImageSendMessage(
        original_content_url= msg,
        preview_image_url= msg
      )
      background_tasks.add_task(line_bot_api.push_message, user_id, image_message)
    else:
      flex_message = FlexSendMessage(alt_text='Flex Msg', contents=msg)
      background_tasks.add_task(line_bot_api.push_message, user_id, flex_message)
    return {'def':'pushMessage','msg':msg}
  except LineBotApiError as e:
    raise HTTPException(status_code=400, detail=msg)