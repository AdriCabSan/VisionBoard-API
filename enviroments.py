import json

with open('config.json', 'r') as f:
    config = json.load(f)

slack_bot_token = config['SLACK']['BOT_TOKEN']
slack_user_token = config['SLACK']['USER_TOKEN'] 
trello_key = config['TRELLO']['API_KEY']
trello_api_secret = config['TRELLO']['API_SECRET']
trello_token = config['TRELLO']['TOKEN']

