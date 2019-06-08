from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
import database


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World I'm WhatsAppBOT2 that supplies movies and series description!"


@app.route("/smss", methods=['POST'])
def sms_reply():
    print(request.form)

    msg = request.form.get('Body')
    sender = request.form.get('From')
    database.initialize_db()

    resp = MessagingResponse()
    news, type1, str1, poster = fetch_reply(msg, sender)

    if(type1 == 'movie'):
        resp.message(str1).media(poster)
        database.insert_db(news)
    elif(type1 == 'series'):
        resp.message(str1).media(poster)
    elif(type1 == 'favorite'):
        resp.message(str1)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
