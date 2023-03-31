def test_generate_checkin_code(client, auth, request):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    checking_code_response = client.post('/api/v1/module-lessons/1', headers=context)
    assert checking_code_response.status_code == 200
    assert "code" in checking_code_response.json.keys()
    request.config.cache.set('shared', checking_code_response.json['code'])
    assert b"error" not in checking_code_response.json

