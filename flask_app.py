from flask import Flask
from datetime import datetime
from Slack import SlackMessenger
from BackEnd-Trello import TrelloVision

app = Flask(__name__)

slack = SlackMessenger()
slack.get_users_id()


@app.route("/own",methods=['post'])
def info():    
  	print(request.get_json())
    json = request.get_json()
    user = json['event']['user']    
    if request.headers.get('x-slack-retry-num') == '1':
   		slack.send_direct_message(user, "Hola, " + slack.user_names[user] + " como vas" )    
    return request.get_json()['challenge'] , 200