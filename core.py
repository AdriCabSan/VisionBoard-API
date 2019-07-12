from flask import Flask
from datetime import datetime
from Slack import SlackMessenger
from Trello import VisionTrello
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"
@app.route("card/")
def getPointsOfCard(card_name, open_character, closed_character):  
    return VisionTrello.get_points_of_a_card(card_name,open_character,closed_character)
   

#This will show you the percentage of recommendation for each person in the board to make some cards based on their experience with the card labels that they did
@app.route("/card/<point>")
def showingRecommendations(board):
    
#This will show you a recommended card for a given member id within the limit based on your experience working with other card
@app.route("/card/<member>")
def recomendCardToMember(board):
@app.route("/card/<point>")
def respectColumnRules(board):
@app.route("/card/<point>")
def getPointsOfColumn(board):
    return ret
@app.route("card/<point>")
def get(board, column_name):
    return ret

@app.route("card/<point>")
def getMemberId(member_name):
  
@app.route("/sprint/<point>")
def predictSprintPoints(board):