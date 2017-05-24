from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('YS6WB+fDoCYL7GdOQGqFgG508DdCpVx6magUNF1+PUuocWnsiWDNMnEet1uYuhvwnd3MK9JIsB41ZLVDjoAOeQ38ND3c01HtuQdF+C4pL94u1D0mEVNPlmrtnI3mjkTXD3o94bs91wWEWyB6rGetSgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('19c221abfb21900ec4dc469df4992f79')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
