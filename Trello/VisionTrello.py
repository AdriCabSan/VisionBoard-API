from trello import TrelloClient
import datetime
import pytz
import numpy as np
import json
import enviroments

client = TrelloClient(
    api_key=enviroments.trello_key,
    api_secret=enviroments.trello_api_secret,
    token=enviroments.trello_token
)


class VisionTrello:
    def __init__(self, all_boards,
                 index_board,
                 member_fullname = '',
                 member_id = '',
                 experience_columns = [],
                 filter_columns = [],
                 limit = 0,
                 sprint_prefix = '',
                 end_date_of_sprint = datetime.datetime(1900, 1, 1).date(),
                 sprint_limit = 0):
        self.all_boards = all_boards
        self.index_board = index_board
        self.member_fullname = member_fullname
        self.member_id = member_id
        self.experience_columns = experience_columns
        self.filter_columns = filter_columns
        self.limit = 0
        self.sprint_prefix = ''
        self.end_date_of_sprint = end_date_of_sprint
        self.sprint_limit = sprint_limit


#This will give you a set of cards that have not been moved during sometime that you set
def card_not_taken(board):
    my_board = board.all_boards[board.index_board]
    all_columns = my_board.list_lists()
    for column in all_columns:
        if column.name in board.filter_columns:
            cards = column.list_cards()
            for card in cards:
                days_elapsed = (pytz.utc.localize(datetime.datetime.utcnow()) - card.dateLastActivity).days
                if days_elapsed >= board.limit:
                    print("This card has not been moved during the last " + str(days_elapsed) + " days from the column " + column.name + " D:")
                    print("Card name: " + card.name)


def get_points_of_a_card(card_name, open_character, closed_character):
    index = card_name.find(open_character)
    card_len = len(card_name)
    ret = 0
    if index != -1:
        index += 1
        while index < card_len and card_name[index] != closed_character:
            ret *= 10
            ret += (ord(card_name[index]) - 48)
            index += 1
    return ret


#This will show you the percentage of recommendation for each person in the board to make some cards based on their experience with the card labels that they did
def showing_recommendations(board):
    my_board = board.all_boards[board.index_board]
    dict = {}
    all_columns = my_board.list_lists()
    for column in all_columns:
        if column.name in board.experience_columns:
            cards = column.list_cards()
            for card in cards:
                points = get_points_of_a_card(card.name, '[', ']')
                points = 1
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
        if column.name in board.filter_columns:
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


#This will show you a recommended card for a given member id within the limit based on your experience working with other card
def recommend_a_card_for_a_member(board):
    my_board = board.all_boards[board.index_board]
    dict = {}
    all_columns = my_board.list_lists()
    max_experience_estimated = 0
    save_card_estimated = {}
    max_experience_not_estimated = 0
    save_card_not_estimated = {}
    for column in all_columns:
        if column.name in board.experience_columns:
            cards = column.list_cards()
            for card in cards:
                points = get_points_of_a_card(card.name, '[', ']')
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
        if column.name in board.filter_columns:
            cards = column.list_cards()
            for card in cards:
                estimated_points = get_points_of_a_card(card.name, '(', ')')
                if(estimated_points <= board.sprint_limit):
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
                            if id_member == board.member_id:
                                actual_experience = all_sums[id_member] * 100 / sum_maxi
                                if(estimated_points == 0):
                                    if (max_experience_not_estimated < actual_experience):
                                        max_experience_not_estimated = actual_experience
                                        save_card_not_estimated[0] = card
                                else:
                                    if (max_experience_estimated < actual_experience):
                                        max_experience_estimated = actual_experience
                                        save_card_estimated[0] = card
    if len(save_card_estimated) > 0:
        print('We recommend you this card ' + save_card_estimated[0].name + ' url = ' + save_card_estimated[0].url + ' your percentage recommendation is about ' + str(max_experience_estimated) + ' %')
    elif len(save_card_not_estimated) > 0:
        print('This card is not estimated but we recommend you this card ' + save_card_not_estimated[0].name + ' url = ' + save_card_not_estimated[0].url + ' your percentage recommendation is about ' + str(max_experience_not_estimated) + ' %')
    else:
        print('We have nothing to recommend you :(, please contact with your leader to see what`s next!')


def respect_column_rules(board):
    my_board = board.all_boards[board.index_board]
    all_columns = my_board.list_lists()
    for column in all_columns:
        limit_cards = get_points_of_a_card(column.name, '{', '}')
        if limit_cards > 0:
            cards = column.list_cards()
            number_of_cards_in_column = len(cards)
            if number_of_cards_in_column > limit_cards:
                print('You have exceeded the number of cards on the column of ' + column.name + ' you have right now ' + str(number_of_cards_in_column) + ' cards when the limit = ' + str(limit_cards))


def get_points_of_column(board):
    my_board = board.all_boards[board.index_board]
    all_columns = my_board.list_lists()
    ret = 0
    for column in all_columns:
        if column.name == board.filter_columns:
            cards = column.list_cards()
            for card in cards:
                ret += get_points_of_a_card(card.name, '[', ']')
            break
    return ret


def get_points_of_column_of_member(board, column_name):
    my_board = board.all_boards[board.index_board]
    all_columns = my_board.list_lists()
    ret = 0
    for column in all_columns:
        if column.name == column_name:
            cards = column.list_cards()
            for card in cards:
                for id_members in card.idMembers:
                    if(id_members == board.member_id):
                        ret += get_points_of_a_card(card.name, '[', ']')
                        break
            break
    return ret


def get_memberid(member_name):
    with open('id_members.json') as f:
        data = json.load(f)
        id_member = data[member_name]
        return id_member


def predict_sprint_points(board):
    ret = 0
    id_member = board.member_id
    my_board = board.all_boards[board.index_board]
    all_columns = my_board.list_lists()
    dict = {}
    for column in all_columns:
        index = column.name.find(board.sprint_prefix)
        column_len = len(column.name)
        if index != -1:
            index += 1
            sprint_number = 0
            while index < column_len and column.name[index].isdigit():
                sprint_number *= 10
                sprint_number += (ord(column.name[index]) - 48)
                index += 1
            sprint_points = get_points_of_column_of_member(board, column.name)
            if sprint_points > 0:
                dict[sprint_number] = sprint_points
    X = []
    Y = []
    remaining_days = (board.end_date_of_sprint.date() - datetime.datetime.today().date()).days
    for key in dict:
        X.append(key)
        Y.append(dict[key])
    if len(dict) > 1:
        X = np.array([np.ones(len(X)), X]).T
        B = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
        predicted_performance = B[0] + B[1] * (len(dict) + 1)
        remaining_points = predicted_performance * remaining_days / 10
        ret = remaining_points
        print('points that i could do during this sprint = ' + str(remaining_points))
    elif len(dict) == 1:
        ret = Y[0]
        ret *= remaining_days
        ret /= 10
        print('Just a spring of ' + str(Y[0]) + ' points')
    else:
        print('Nothing to do')
    return ret


def rdebug(board):
    my_board = board.all_boards[board.index_board]
    a = my_board.get_members()
    print(a)
    for member in a:
        f = open("jiji.txt", 'a+')
        f.write(str(member.full_name + '\n'))
        f.write(str(member.id + '\n'))
        print(member.full_name)
        print(member.id)


working_board = VisionTrello(all_boards = client.list_boards(),
                      index_board = 0,
                      filter_columns = ['Sprint Backlog'],
                      limit = 7)

#card_not_taken(working_board)

working_board.experience_columns = ['Done', 'S2', 'S1', 'Card hasta el 7 JUN', 'Docs Done']

working_board.filter_columns = ['Sprint Backlog', 'Pre Planning']

#showing_recommendations(working_board)

working_board.sprint_prefix = 'S'

working_board.member_fullname = 'Arturo Hinojosa Reyes'

working_board.end_date_of_sprint = datetime.datetime(2019, 7, 15)

working_board.member_id = get_memberid(working_board.member_fullname)

#sprint_limit = predict_sprint_points(working_board)

#working_board.sprint_limit = sprint_limit

#recommend_a_card_for_a_member(working_board)

respect_column_rules(working_board)

#rdebug(client.list_boards(), 0)



print("Hello ecaresoft!")
