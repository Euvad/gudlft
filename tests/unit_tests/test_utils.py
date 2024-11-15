from datetime import datetime

def test_sort_competitions_by_date(sort_competitions, competition_data):
    # Appel de la fonction mockée ou réelle (via la fixture sort_competitions)
    past_events, upcoming_events = sort_competitions(competition_data)

    # Vérifications des types de retour
    assert isinstance(past_events, list), "La variable 'past_events' n'est pas une liste"
    assert isinstance(upcoming_events, list), "La variable 'upcoming_events' n'est pas une liste"
    assert len(past_events) + len(upcoming_events) == len(competition_data)

    # Vérification des dates des événements passés
    if past_events:
        assert datetime.strptime(past_events[0]['date'], '%Y-%m-%d %H:%M:%S') < datetime.now()

    # Vérification des dates des événements futurs
    if upcoming_events:
        assert datetime.strptime(upcoming_events[0]['date'], '%Y-%m-%d %H:%M:%S') >= datetime.now()

def test_initialize_booked_places_structure(initialize_bookings, competition_data, club_data):
    # Appel de la fonction mockée ou réelle (via la fixture initialize_bookings)
    bookings = initialize_bookings(competition_data, club_data)

    # Vérifications des propriétés de la structure des réservations
    assert isinstance(bookings, list), "La structure de données 'bookings' n'est pas une liste"
    assert len(bookings) == len(competition_data) * len(club_data)
    assert bookings[0]['booked'] == [0, club_data[0]['name']]

def test_update_booked_places_list(update_bookings, initialize_bookings, competition_data, club_data):
    required_places = 2

    # Appel de la fonction initialize_bookings pour générer les données initiales
    initial_bookings = initialize_bookings(competition_data, club_data)

    # Appel de la fonction update_bookings pour mettre à jour les données
    updated_bookings = update_bookings(
        competition_data[0],
        club_data[0],
        initial_bookings,
        required_places
    )

    # Vérifications sur la structure mise à jour
    assert isinstance(updated_bookings, list), "La structure de données 'updated_bookings' n'est pas une liste"
    assert len(updated_bookings) == len(initial_bookings)
    assert updated_bookings[0]['booked'] == [required_places, club_data[0]['name']]
