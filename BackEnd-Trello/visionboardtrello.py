from trello import TrelloClient
#import tensorflow as tf
import datetime
import pytz
import numpy as np
import json


client = TrelloClient(
    api_key='65e3c96c34e8543f5f79ddad3a591742',
    api_secret='36b872e6d755ff2b3d37293e9dcacb467c8db1ee8b560d358be75001068c5274',
    token='084ab842600d494065dfe16562374d9c27dd465ccb91133560a07189f2c8d021',
)

#This will give you a set of cards that have not been moved during sometime that you set
def card_not_taken(all_boards, index_board, filter_columns, limit):
    my_board = all_boards[index_board]
    all_columns = my_board.list_lists()
    for column in all_columns:
        if column.name in filter_columns:
            cards = column.list_cards()
            for card in cards:
                days_elapsed = (pytz.utc.localize(datetime.datetime.utcnow()) - card.dateLastActivity).days
                if days_elapsed >= limit:
                    print("This card has not been moved during the last " + str(days_elapsed) + " days from the column " + column.name + " D:")
                    print("Card name: " + card.name)


def get_points_of_a_card(card_name):
    index = card_name.find('[')
    card_len = len(card_name)
    ret = 0
    if index != -1:
        index += 1
        while index < card_len and card_name[index] != ']':
            ret *= 10
            ret += (ord(card_name[index]) - 48)
            index += 1
    return ret


#This will show you the percentage of recommendation for each person in the board to make some cards based on their experience with the card labels that they did
def recommend_a_card(all_boards, index_board, experience_columns, filter_columns):
    my_board = all_boards[index_board]
    dict = {}
    all_columns = my_board.list_lists()
    for column in all_columns:
        if column.name in experience_columns:
            cards = column.list_cards()
            for card in cards:
                points = get_points_of_a_card(card.name)
                #print('This cards has ' + str(points) + ' points with the name : ' + card.name)
                for label in card._labels:
                    for id_member in card.idMembers:
                        if dict.get(label.name):
                            if dict[label.name].get(id_member):
                                dict[label.name][id_member] += points
                            else:
                                dict[label.name][id_member] = points
                        else:
                            dict[label.name] = {}
                            dict[label.name][id_member] = points
    for column in all_columns:
        if column.name in filter_columns:
            cards = column.list_cards()
            for card in cards:
                print('Statistics for the card ' + card.name + '\n')
                sum_maxi = 0
                all_sums = {}
                for label in card._labels:
                    maxi = 0
                    for id_member in dict[label.name]:
                        if all_sums.get(id_member):
                            all_sums[id_member] += dict[label.name][id_member]
                        else:
                            all_sums[id_member] = dict[label.name][id_member]
                        maxi = max(maxi, dict[label.name][id_member])
                    sum_maxi += maxi
                if sum_maxi > 0:
                    for id_member in all_sums:
                        print(client.get_member(id_member).full_name + ' has a recommendation to do this card by ' + str(all_sums[id_member] * 100 / sum_maxi) + ' %')
                else:
                    print('No one has implement this before :O')
                print('')
#    for label in dict:
#        print('Label : ' + label)
#        for id_member in dict[label]:
#            print(client.get_member(id_member).full_name)

def respect_column_rules():
    print('To do Peer Review{8} receiving the names of the columns with {}')


def show_columns_in_board(all_boards, index_board):
    print('To do')


def get_points_of_column(all_boards, index_board, filter_column):
    my_board = all_boards[index_board]
    all_columns = my_board.list_lists()
    ret = 0
    for column in all_columns:
        if column.name == filter_column:
            cards = column.list_cards()
            for card in cards:
                ret += get_points_of_a_card(card.name)
            break
    return ret


def get_points_of_column_of_member(all_boards, index_board, filter_column, id_member):
    my_board = all_boards[index_board]
    all_columns = my_board.list_lists()
    ret = 0
    for column in all_columns:
        if column.name == filter_column:
            cards = column.list_cards()
            for card in cards:
                for id_members in card.idMembers:
                    if(id_members == id_member):
                        ret += get_points_of_a_card(card.name)
                        break
            break
    return ret


def get_memberid(member_name):
    with open('id_members.json') as f:
        data = json.load(f)
        id_member = data[member_name]
        return id_member


def predict_sprint_points(all_boards, index_board, sprint_prefix, member_name):
    id_member = get_memberid(member_name)
    my_board = all_boards[index_board]
    all_columns = my_board.list_lists()
    dict = {}
    for column in all_columns:
        index = column.name.find(sprint_prefix)
        column_len = len(column.name)
        if index != -1:
            index += 1
            sprint_number = 0
            while index < column_len and column.name[index].isdigit():
                sprint_number *= 10
                sprint_number += (ord(column.name[index]) - 48)
                index += 1
            sprint_points = get_points_of_column_of_member(all_boards, index_board, column.name, id_member)
            if sprint_points > 0:
                dict[sprint_number] = sprint_points
    X = []
    Y = []
    for key in dict:
        X.append(key)
        Y.append(dict[key])
        print('key = ' + str(key) + ' value = ' + str(dict[key]))
    if len(dict) > 1:
        X = np.array([np.ones(len(X)), X]).T
        B = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
        print('Bias = ' + str(B[0]))
        print('Coefficient = ' + str(B[1]))
        predicted_performance = B[0] + B[1] * (len(dict) + 1)
        print('Predicted performance = ' + str(predicted_performance))
    elif len(dict) == 1:
        print('Just a spring of ' + str(Y[0]) + ' points')
    else:
        print('Nothing to do')


#def rdebug(all_boards, index_board, member_name):
#    my_board = all_boards[index_board]
#    a = my_board.get_members()
#    print(a)
#    for member in a:
#        f = open("jiji.txt", 'a+')
#        f.write(member.full_name)
#        f.write(member.id)
#        print(member.full_name)
#        print(member.id)

def rdebug(all_boards, index_board):
    print('zzz...')


#card_not_taken(client.list_boards(), 0, ['Sprint Backlog'], 7)
#recommend_a_card(client.list_boards() , 0, ['Done', 'S2', 'S1', 'Card hasta el 7 JUN', 'Docs Done'], ['Sprint Backlog', 'Pre Planning'])
#rdebug(client.list_boards(), 0, 'Arturo Hinojosa Reyes')
predict_sprint_points(client.list_boards(), 0, 'S', 'Arturo Hinojosa Reyes')


print("Hello ecaresoft!")
