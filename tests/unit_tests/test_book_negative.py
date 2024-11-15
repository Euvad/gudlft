def test_purchase_negative_places(client, mock_data, competition_data, club_data):
    response = client.post('/purchasePlaces', data={
        'competition': competition_data[0]['name'],  # Utilisation des données de la fixture
        'club': club_data[0]['name'],  # Utilisation des données de la fixture
        'places': '-1'  # Valeur négative pour le test
    })
    
    # Vérification du message d'erreur et du code de statut
    assert b'Please enter a positive number of places.' in response.data
    assert response.status_code == 400
