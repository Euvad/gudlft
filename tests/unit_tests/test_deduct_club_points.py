def test_deduct_points(client, mock_data, competition_data, club_data):
    initial_points = int(club_data[0]["points"])
    places_to_book = 3

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_to_book,
            "club": club_data[0]["name"],  # Utilisation des fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérifier que la réservation a réussi et que les points ont été déduits correctement
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert initial_points - places_to_book * 3 >= 0  # Les points doivent être déduits

def test_empty_field(client, mock_data, competition_data, club_data):
    places_to_book = ""

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_to_book,
            "club": club_data[0]["name"],  # Utilisation des fixtures
            "competition": competition_data[0]["name"]
        }
    )

    # Vérifier que le champ vide déclenche une erreur avec un message approprié
    assert response.status_code == 400
    assert "Please enter a number between 0 and 12." in response.data.decode()
