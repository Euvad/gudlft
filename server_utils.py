# **************************************************************************** #
#                                                                              #
#                                                         ::::::::   ::::::::  #
#    server_utils.py                                    :+:    :+: :+:    :+:  #
#                                                             +:+       +:+    #
#    By: Vadim32 <vad.studio@icloud.com>                  +#++:      +#+       #
#                                                           +#+   +#+          #
#    Created: 2024/11/04 13:51:33 by Vadim32        #+#    #+#  #+#            #
#    Updated: 2024/11/15 16:38:46 by Vadim32        ########  ##########       #
#                                                                              #
# **************************************************************************** #

from datetime import datetime
import json

def load_clubs():
    with open('clubs.json') as file:
        return json.load(file)['clubs']

def load_competitions():
    with open('competitions.json') as file:
        return json.load(file)['competitions']

def sort_competitions_date(competitions):
    past_competitions, upcoming_competitions = [], []
    
    for competition in competitions:
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date < datetime.now():
            past_competitions.append(competition)
        else:
            upcoming_competitions.append(competition)

    return past_competitions, upcoming_competitions

def initialize_booked_places(competitions, clubs):
    return [{'competition': comp['name'], 'booked': [0, club['name']]} for comp in competitions for club in clubs]

def update_booked_places(competition, club, bookings, requested_places):
    for booking in bookings:
        if booking['competition'] == competition['name'] and booking['booked'][1] == club['name']:
            if booking['booked'][0] + requested_places <= 12:
                booking['booked'][0] += requested_places
            break

    return bookings
