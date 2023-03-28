
def test_login(client, auth):
    response = auth.login()
    assert response.status_code == 200
    assert b"error"  not in response.json
    
def test_users(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    assert client.get('/api/v1/auth/users', headers=context).status_code == 200
    
def test_user_detail(client, auth):
    response = auth.login()
    assert response.status_code == 200
    id = response.json["user_id"]
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    assert client.get('/api/v1/auth/users/'+f"{id}", headers=context).status_code == 200
