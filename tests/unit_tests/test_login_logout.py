def test_user_login(client):
    response = client.get("/")
    assert response.status_code == 200

def test_user_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302
