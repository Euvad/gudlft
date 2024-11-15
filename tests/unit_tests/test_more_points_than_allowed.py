def test_points_sufficient_for_booking(client, mock_data, club_data, competition_data):
    # Simulation d'une réservation de places avec suffisamment de points
    places_requested = 3  # Chaque place coûte 3 points, donc 9 points nécessaires

    # Envoi de la requête POST pour la réservation
    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_requested,
            "club": club_data[0]["name"],  # Utilisation des données simulées via fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification de la réservation réussie
    assert response.status_code == 200, "Le serveur n'a pas retourné un code de succès attendu (200)."
    assert "Great-booking complete!" in response.data.decode(), (
        "Le message de confirmation attendu n'est pas présent dans la réponse."
    )


def test_points_insufficient_for_booking(client, mock_data, club_data, competition_data):
    # Simulation d'une réservation de places avec des points insuffisants
    places_requested = 11  # Chaque place coûte 3 points, donc 15 points nécessaires (10 points disponibles)

    # Envoi de la requête POST pour la réservation
    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_requested,
            "club": club_data[1]["name"],  # Utilisation des données simulées via fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification de l'échec de la réservation
    assert response.status_code == 400, "Le serveur n'a pas retourné un code d'erreur attendu (400)."
    assert "have enough points." in response.data.decode(), (
        "Le message d'erreur attendu pour points insuffisants n'est pas présent dans la réponse."
    )
