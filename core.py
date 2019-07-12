from flask import Flask
from datetime import datetime
from Slack import SlackMessenger
from BackEnd-Trello import TrelloVision

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/<card>/<point>")
def getCardPoints():
  

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content