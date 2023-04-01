   
def test_get_module_lessons(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    module_lessons_response = client.get('/api/v1/modules/1', headers=context)
    assert module_lessons_response.status_code == 200
    assert "success" in module_lessons_response.json.keys()
    assert "data" in module_lessons_response.json.keys()
    assert b"error" not in module_lessons_response.json
    
def test_get_staff_lessons(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    staff_lessons_response = client.get('/api/v1/modules/lessons', headers=context)
    assert staff_lessons_response.status_code == 200
    assert "success" in staff_lessons_response.json.keys()
    assert "data" in staff_lessons_response.json.keys()
    assert b"error" not in staff_lessons_response.json
