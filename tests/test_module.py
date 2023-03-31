   
def test_get_module_lessons(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    module_lessons_response = client.get('/api/v1/modules/1', headers=context)
    assert module_lessons_response.status_code == 200
    assert b"error" not in module_lessons_response.json
