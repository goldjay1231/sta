from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
# from linebot.models import *
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('3Us2C2fOXlfLeNRBuGUM4GJEnDVqpTiPn2HhMgKRlZi3tY/OYLVI1c4kYcXMNxuQKKxPyoAyFfsFxy4VZcH0ZkfWXvx7ag8p9N3Vbph59yb6BQrN11DOF7b2uA+TTqNXFGV+Yhx4cDrfdQ7GHExpWQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('5d32888a07fb31ad6b7c004a6a44c5d0')

line_bot_api.push_message('Ua4ff9767f1ae0ea5fe3aa61e5051fde5',
                          TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)