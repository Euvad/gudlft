import html
def test_booking_under_limit(client, mock_data, club_data, competition_data):
    """Test: Réserver un nombre de places dans la limite autorisée."""
    places_requested = 1

    # Envoi de la requête POST
    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_requested,
            "club": club_data[0]["name"],  # Utilisation des données simulées via fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification de la réservation réussie
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()

def test_booking_exceeds_limit_once(client, mock_data, club_data, competition_data):
    """Test: Réserver un nombre de places dépassant la limite autorisée en une seule requête."""
    places_requested = 13  # Plus que la limite de 12

    # Envoi de la requête POST
    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_requested,
            "club": club_data[0]["name"],
            "competition": competition_data[0]["name"]
        }
    )
    print(response.data.decode())
    # Vérification du refus de réservation
    assert response.status_code == 400
    # Utilisation de html.unescape pour éviter les problèmes d'encodage HTML
    response_data = html.unescape(response.data.decode())
    # Vérification que le message d'erreur est bien présent
    assert "You can't book more than 12 places in a competition." in response_data

def test_booking_exceeds_limit_accumulative(client, mock_data, club_data, competition_data):
    """Test: Réserver un nombre de places en deux étapes dépassant la limite cumulée."""
    places_requested_first = 8  # Première réservation valide

    # Envoi de la première requête POST
    response_first = client.post(
        "/purchasePlaces",
        data={
            "places": places_requested_first,
            "club": club_data[0]["name"],
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification de la première réservation réussie
    assert response_first.status_code == 200, "La première réservation valide a échoué."
    assert "Great-booking complete!" in response_first.data.decode(), (
        "Le message de confirmation pour la première réservation est absent."
    )

    places_requested_second = 5  # Deuxième réservation qui dépasse la limite cumulée (8 + 5 > 12)

    # Envoi de la deuxième requête POST
    response_second = client.post(
        "/purchasePlaces",
        data={
            "places": places_requested_second,
            "club": club_data[0]["name"],
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification du refus de la réservation supplémentaire
    assert response_second.status_code == 400
    response_data = html.unescape(response_second.data.decode())
    # Vérification que le message d'erreur est bien présent
    assert "You can't book more than 12 places in a competition." in response_data