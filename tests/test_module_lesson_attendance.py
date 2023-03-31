
def test_student_self_attendance_registration(client, auth, request):
    response = auth.loginStudent()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    checkin_code = request.config.cache.get('shared', None)
    data ={
        "checkin_code" : checkin_code
    }
    checking_code_response = client.post('/api/v1/module-lessons-attendance/1', json=data, headers=context)
    assert checking_code_response.status_code == 201
    
