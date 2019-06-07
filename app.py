from flask import Flask, request 
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply 


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World I'm WhatsAppBOT for that supplies movies and series description"

@app.route("/sms", methods=['POST'])
def sms_reply():
    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')

    print(msg)
    resp = MessagingResponse()
    str1,poster= fetch_reply(msg,sender)
    resp.message(str1).media(poster)
   
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)