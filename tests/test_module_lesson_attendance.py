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
    
