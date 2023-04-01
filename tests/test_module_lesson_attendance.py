from .test_module_lesson import test_generate_checkin_code
def test_student_self_attendance_registration(client, auth):
    response = auth.loginStudent()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }

    checkin_code= test_generate_checkin_code(client, auth)
    data ={
        "checkin_code" : checkin_code
    }
    checking_code_response = client.post('/api/v1/module-lessons-attendance/1', json=data, headers=context)
    assert checking_code_response.status_code == 201
    

def test_bulk_attendance_registration(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }

    data ={
        "student_list" : [{"id":1, "attendance_status": "P"}, {"id":2, "attendance_status": "P"}, {"id":3, "attendance_status": "O"}]
    }
    checking_code_response = client.post('/api/v1/module-lessons-attendance/staff/1', json=data, headers=context)
    assert checking_code_response.status_code == 201
    
def test_get_module_lesson_attendance(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    module_lessons_response = client.get('/api/v1/module-lessons-attendance/1', headers=context)
    assert module_lessons_response.status_code == 200
    assert "success" in module_lessons_response.json.keys()
    assert "data" in module_lessons_response.json.keys()
    assert b"error" not in module_lessons_response.json
    
def test_update_module_lesson_attendance(client, auth):
    response = auth.login()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    data = {"status" : "P" }
    update_attendance_response = client.put('/api/v1/module-lessons-attendance/1/students/5', json=data, headers=context)
    assert update_attendance_response.status_code == 200
    assert "success" in update_attendance_response.json.keys()
    assert b"error" not in update_attendance_response.json

    
