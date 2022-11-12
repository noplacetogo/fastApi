import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import settings
sys.path.append('..')


class EMAIL:
    @classmethod
    def send(cls, receiver: str = "sjp4fu6@gmail.com",
                  sender: dict = {'sender': settings.EMAIL.sender, 'sender_token': settings.EMAIL.sender_token},
                  subject: str = '測試信件', detail: str = '測試內容'):
        content = MIMEMultipart()  # 建立MIMEMultipart物件
        content["subject"] = subject  # 郵件標題
        content["from"] = sender['sender']  # 寄件者
        content["to"] = receiver  # 收件者
        html = MIMEText(detail, 'html')
        content.attach(html)  # 郵件內容
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login(sender['sender'], sender['sender_token'])  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)


