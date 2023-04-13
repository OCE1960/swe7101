def test_student_attendance_record(client, auth):
    response = auth.loginStudent()
    assert response.status_code == 200
    token = "Bearer "+response.json["access_token"]
    context = { "Authorization": token }
    student_attendance_response = client.get('/api/v1/module-lessons-attendance/student-attendance', headers=context)
    assert student_attendance_response.status_code == 200
    assert b"error" not in student_attendance_response.json