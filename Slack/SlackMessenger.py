class SlackMessenger:
    bot_token = 'xoxb-685233796401-693744259798-OtXlb1bChcEo98YSx6fiFhbL'
    user_token= 'xoxp-685233796401-691580016560-680179250178-75c9bd71f7c4b2aec022e67fcbcad359'
    
    slack = None
    
    user_handlebar = '%user'

    templates = {'recommendation' : ['Okay %user. I ve found a card this card %card']}
    
    channels = {'user' : 'channel'}
    user_names = {'name' : ' id'}

    def __init__ (self,is_bot=True):
        if is_bot:
            self.slack = Slacker(self.bot_token)
        else: 
            self.slack = Slacker(self.user_token)
        return
    
    def send_message_channel(self,channel,message):
        self.slack.chat.post_message(channel, message)
        
    def get_channels_id (self):
        l = self.slack.conversations.list()
        return [{i['name']:i['id']} for i in l.body['channels']]

    def get_users_id (self):
        l = self.slack.users.list()
        for i in l.body['members']:
            self.user_names[i['id']] = i['name']

    def send_direct_message(self,user_id,message):
        private_channel_id = self.slack.im.open(user=user_id).body['channel']['id']
        self.channels[user_id] = private_channel_id
        self.send_message_channel(private_channel_id,message)
        
    def bind_message (self,template,token,value):
        return template.replace(token,value)
    
    