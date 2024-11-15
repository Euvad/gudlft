def test_booking_exceeds_availability(client, mock_data, club_data, competition_data):
    # Réservation de plus de places que disponibles
    requested_places = 16 # Nombre de places demandé dépasse les places disponibles (par défaut : 5)

    # Envoi de la requête POST
    response = client.post(
        "/purchasePlaces",
        data={
            "places": requested_places,
            "club": club_data[0]["name"],  # Utilisation des données simulées via fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification du refus de réservation
    assert response.status_code == 400, "Le serveur n'a pas retourné un code d'erreur attendu (400)."
    assert "Not enough places available." in response.data.decode(), (
        "Le message d'erreur attendu pour les places non disponibles n'est pas présent dans la réponse."
    )


def test_booking_within_availability(client, mock_data, club_data, competition_data):
    # Réservation d'un nombre de places dans la limite des places disponibles
    requested_places = 1  # Nombre de places demandé est dans la limite disponible

    # Envoi de la requête POST
    response = client.post(
        "/purchasePlaces",
        data={
            "places": requested_places,
            "club": club_data[0]["name"],  # Utilisation des données simulées via fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification de la réservation réussie
    assert response.status_code == 200, "Le serveur n'a pas retourné un code de succès attendu (200)."
    assert "Great-booking complete!" in response.data.decode(), (
        "Le message de confirmation de réservation n'est pas présent dans la réponse."
    )
