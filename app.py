from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply, fetch_reply_favorite
import database


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World I'm WhatsAppBOT that supplies movies and series description!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    print(request.form)

    msg = request.form.get('Body')
    sender = request.form.get('From')
    database.initialize_db()
    print(msg)
    resp = MessagingResponse()
    if 'favorite' in msg:
        favorite_string = fetch_reply_favorite(msg, sender)
        resp.message(favorite_string)
    else:
        news, type1, str1, poster = fetch_reply(msg, sender)
        if(type1 == 'movie'):
            database.insert_db(news)
        if(type1 == 'movie'):
            resp.message(str1).media(poster)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
