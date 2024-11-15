# **************************************************************************** #
#                                                                              #
#                                                         ::::::::   ::::::::  #
#    server.py                                          :+:    :+: :+:    :+:  #
#                                                             +:+       +:+    #
#    By: Vadim32 <vad.studio@icloud.com>                  +#++:      +#+       #
#                                                           +#+   +#+          #
#    Created: 2024/11/04 13:51:28 by Vadim32        #+#    #+#  #+#            #
#    Updated: 2024/11/15 16:50:43 by Vadim32        ########  ##########       #
#                                                                              #
# **************************************************************************** #


#fix la faille avec les nombre negatif
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from server_utils import load_clubs, load_competitions, sort_competitions_date, initialize_booked_places, update_booked_places

app = Flask(__name__)
app.secret_key = 'something_special'
 
# Chargement des données
competitions = load_competitions()
clubs = load_clubs()
past_competitions, present_competitions = sort_competitions_date(competitions)
places_booked = initialize_booked_places(competitions, clubs)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    email = request.form.get('email', '')
    club = next((c for c in clubs if c['email'] == email), None)
    
    if club:
        return render_template(
            'welcome.html',
            club=club,
            past_competitions=past_competitions,
            present_competitions=present_competitions
        )
    else:
        flash("Please enter your email." if email == '' else "No account related to this email.", 'error')
        return render_template('index.html'), 401


@app.route('/book/<competition_name>/<club_name>')
def book(competition_name, club_name):
    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next((c for c in competitions if c['name'] == competition_name), None)

    if not club or not competition:
        flash("Something went wrong-please try again", 'error')
        return render_template('index.html'), 404

    if datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
        flash("This competition is over.", 'error')
        return render_template(
            'welcome.html',
            club=club,
            past_competitions=past_competitions,
            present_competitions=present_competitions
        ), 400

    return render_template('booking.html', club=club, competition=competition)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition_name = request.form['competition']
    club_name = request.form['club']
    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next((c for c in competitions if c['name'] == competition_name), None)

    # if not club or not competition:
    #     flash("Invalid competition or club selected.", 'error')
    #     return redirect(url_for('index')), 404

    try:
        places_requested = int(request.form['places'])

        # Vérification que le nombre de places demandées est positif
        if places_requested < 0:
            flash('Please enter a positive number of places.', 'error')
            return render_template('booking.html', club=club, competition=competition), 400

        # Vérification de la disponibilité des places dans la compétition
        if places_requested > int(competition['numberOfPlaces']):
            flash('Not enough places available.', 'error')
            return render_template('booking.html', club=club, competition=competition), 400

        # Calcul des places déjà réservées pour ce club dans cette compétition
        existing_booking = next(
            (booking for booking in places_booked if booking['competition'] == competition['name'] and booking['booked'][1] == club['name']),
            None
        )
        current_booked_places = existing_booking['booked'][0] if existing_booking else 0
        print(current_booked_places)
        # Vérification de la limite cumulative de 12 places
        if current_booked_places + places_requested > 12:
            flash("You can't book more than 12 places in a competition.", 'error')
            return render_template('booking.html', club=club, competition=competition), 400

        # Vérification des points disponibles pour le club
        elif places_requested * 1 > int(club['points']):
            flash("You don't have enough points.", 'error')
        else:
            # Mise à jour des réservations et des points du club
            update_booked_places(competition, club, places_booked, places_requested)
            competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_requested)
            club['points'] = str(int(club['points']) - (places_requested * 1))
            flash('Great-booking complete!', 'success')
            return render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions
            )

    except ValueError:
        flash('Please enter a number between 0 and 12.', 'error')

    return render_template('booking.html', club=club, competition=competition), 400


@app.route('/viewClubPoints')
def view_club_points():
    club_list = sorted(clubs, key=lambda c: c['name'])
    return render_template('club_points.html', clubs=club_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))




