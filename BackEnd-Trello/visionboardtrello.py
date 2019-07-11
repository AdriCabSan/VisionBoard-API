from trello import TrelloClient
import tensorflow as tf
import datetime
import pytz


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
                if days_elapsed > limit:
                    print("This card has not been moved during the last " + str(days_elapsed) + " days from the column " + column.name + " D:")
                    print("Card name: " + card.name)

#This will show you the percentage of recommendation for each person in the board to make some cards based on their experience with the card labels that they did
def recommend_a_card(all_boards, index_board, experience_columns, filter_columns):
    my_board = all_boards[index_board]
    dict = {}
    all_columns = my_board.list_lists()
    for column in all_columns:
        if column.name in experience_columns:
            cards = column.list_cards()
            for card in cards:
                for label in card._labels:
                    for id_member in card.idMembers:
                        if dict.get(label.name):
                            if dict[label.name].get(id_member):
                                dict[label.name][id_member] += 1
                            else:
                                dict[label.name][id_member] = 1
                        else:
                            dict[label.name] = {}
                            dict[label.name][id_member] = 1
    for column in all_columns:
        if column.name in filter_columns:
            cards =  column.list_cards()
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
                        print(client.get_member(id_member).full_name + ' has a recommendation to do this card by ' + str(all_sums[id_member] / sum_maxi * 100) + '%')
                else:
                    print('No one has implement this before :O')
                print('')
#    for label in dict:
#        print('Label : ' + label)
#        for id_member in dict[label]:
#            print(client.get_member(id_member).full_name)


def rdebug(all_boards, index_board, filter_columns):
    my_board = all_boards[index_board]
    dict = {}
    all_columns = my_board.list_lists()
    for column in all_columns:
        if column.name in filter_columns:
            cards = column.list_cards()
            for card in cards:
                print(card.customFields)


#card_not_taken(client.list_boards(), 0, ['Sprint Backlog'], 6)
#recommend_a_card(client.list_boards() , 0, ['Done', 'S2', 'S1', 'Card hasta el 7 JUN', 'Docs Done'], ['Sprint Backlog', 'Pre Planning'])
rdebug(client.list_boards(), 0, ['S1'])


print("Hello ecaresoft!")
