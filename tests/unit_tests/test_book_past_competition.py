from freezegun import freeze_time

def test_booking_closed_competition(client, mock_data, competition_data, club_data):
    with freeze_time("2025-01-01"):
        response = client.get(
            f"/book/{competition_data[0]['name']}/{club_data[0]['name']}"
        )
        assert response.status_code == 400
        assert "This competition is over." in response.data.decode()

def test_booking_open_competition(client, mock_data, competition_data, club_data):
    with freeze_time("2025-01-01"):
        response = client.get(
            f"/book/{competition_data[1]['name']}/{club_data[0]['name']}"
        )
        assert response.status_code == 200

def test_booking_nonexistent_competition(client, mock_data, club_data):
    response = client.get(
        f"/book/unknown_competition/{club_data[0]['name']}"
    )
    assert response.status_code == 404
    assert "Something went wrong-please try again" in response.data.decode()
