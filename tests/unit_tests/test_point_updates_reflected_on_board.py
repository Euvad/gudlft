def test_points_update(client, mock_data, club_data, competition_data):
    # Récupération des points du club avant la réservation
    club_points_before = int(club_data[0]["points"])
    places_booked = 1
    cost_per_place = 1  # Supposition : Chaque place coûte 3 points

    # Étape 1 : Réservation des places
    response_booking = client.post(
        "/purchasePlaces",
        data={
            "places": places_booked,
            "club": club_data[0]["name"],  # Utilisation des fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérification de la réponse après la réservation
    assert response_booking.status_code == 200
    assert "Great-booking complete!" in response_booking.data.decode()

    # Étape 2 : Vérification des points du club mis à jour
    response_points = client.get("/viewClubPoints")

    # Vérification que la page de points s'affiche correctement
    assert response_points.status_code == 200
    assert f"<td>{club_data[0]['name']}</td>" in response_points.data.decode()

    # Vérification que les points sont correctement mis à jour
    expected_points = club_points_before - places_booked * cost_per_place
    assert f"<td>{expected_points}</td>" in response_points.data.decode()
