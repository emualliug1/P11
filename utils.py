# -*- coding:Utf8 -*-
#############################################
# Programme Flask type
# Auteur: G.T,Nt,2022
#############################################
# Importation de fonction externe :
import json
from datetime import datetime
#############################################
# Définition des constantes
MAX_BOOKED_PLACES = 12
#############################################
# Définition de fonction


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def sorted_old_competitions(competitions):
    old_competitions = []
    for competition in competitions:
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date < datetime.now():
            old_competitions.append(competition)
    return old_competitions


def sorted_new_competitions(competitions):
    new_competitions = []
    for competition in competitions:
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        if competition_date >= datetime.now():
            new_competitions.append(competition)
    return new_competitions


def start_places_reserved(competitions, clubs):
    places_reserved = []
    for competition in competitions:
        for club in clubs:
            places_reserved.append({'competition': competition['name'], 'club': club['name'], 'placesRestantes': 0})
    return places_reserved


def update_places_reserved(competition, club, places_reserved, places_required):
    for item in places_reserved:
        if item['competition'] == competition['name'] and item['club'] == club['name']:
            if item['placesRestantes'] + places_required <= MAX_BOOKED_PLACES:
                item['placesRestantes'] += places_required
            else:
                raise ValueError("vous ne pouvez pas réserver plus de 12 places")
    return places_reserved
