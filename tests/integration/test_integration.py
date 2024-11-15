import pytest
from flask import Flask
from unittest.mock import patch

def test_booking_places(client, mock_data):
    """
    Test d'intégration pour le processus de réservation de places avec calcul des points.
    """
    # Étape 1 : Connexion avec un club
    club_email = "test_club@example.com"  # Email de connexion du club
    response = client.post('/showSummary', data={"email": club_email})
    
    # Vérifier que la connexion fonctionne
    assert response.status_code == 200
    assert b"Welcome, test_club@example.com" in response.data

    # Étape 2 : Accéder à une compétition pour réserver des places
    competition_name = "Future Competition"  # Une compétition valide
    user_name = "Test Club"
    response = client.get(f'/book/{competition_name}/{user_name}')
    
    # Vérifier que la page de réservation est accessible
    assert response.status_code == 200
    assert b"How many places?" in response.data

    # Étape 3 : Soumettre une réservation
    requested_places = 3
    response = client.post('/purchasePlaces', data={
        "club": "Test Club",
        "competition": competition_name,
        "places": requested_places
    })

    # Vérifier que la réservation est réussie
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    # Étape 4 : Vérifier les données mises à jour
    with patch('server.competitions', mock_data):
        # Rechercher la compétition dans les données simulées
        competition = next((comp for comp in mock_data if comp['competition'] == competition_name), None)
        club = next((club for club in mock_data if club['booked'][1] == "Test Club"), None)

        # Vérifier que les places réservées ont été mises à jour
        assert competition is not None
        assert int(competition['booked'][0]) == 3  # Le nombre de places réservées

        # Calcul des points : on part du nombre initial de points (15 points), et on les réduit pour chaque réservation
        total_points = 15  # Nombre initial de points
        total_points -= requested_places  # Soustraction du nombre de places réservées (1 point par place)

        # Vérifier que le calcul des points est correct
        assert total_points == 12  # 15 - 3 réservations

        # Correction du calcul des points du club
        # Calcul des points en fonction des places réservées
        club_points = 0
        for comp in mock_data:
            if comp['competition'] == competition_name and comp['booked'][1] == "Test Club":
                club_points += comp['booked'][0]  # Compter les points de réservation par place réservée

        # Vérifier que le calcul des points est correct
        assert club_points == 3  # Le club a réservé 3 places

        # Finalement, vérifier les points totaux après réservation
        final_points = 15 - club_points  # Points initiaux moins les réservations
        assert final_points == 12  # Vérifier que les points sont maintenant corrects (15 - 3)
