def test_known_email_login(client, mock_data, club_data):
    response = client.post("/showSummary", data={"email": club_data[0]["email"]})
    assert response.status_code == 200
    assert club_data[0]["email"] in response.data.decode()

def test_unknown_email_login(client, mock_data):
    response = client.post("/showSummary", data={"email": "unknown@example.com"})
    assert response.status_code == 401
    assert "No account related to this email." in response.data.decode()

def test_missing_email_field(client, mock_data):
    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 401
    assert "Please enter your email." in response.data.decode()
