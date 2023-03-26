from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from .. import db
from ..models.User import User
from ..models.Staff import Staff
from ..models.Student import Student
from ..models.Course import Course

password = 'password'
user_password = generate_password_hash(password, 'sha256') 

user_staff_data =[{'username':'francis', 'email':'francis@bolton.ac.uk', 'telephone':'7812458923', 'firstname': 'Francis', 'lastname': 'Morris', 'staffcode': '7813'},
            {'username':'ibtisam', 'email':'ibtisam@bolton.ac.uk', 'telephone':'7812452544','firstname': 'Ibtisam', 'lastname': 'Mogul', 'staffcode': '7814'},     
            ]

user_student_data =[
            {'username':'rozmin', 'email':'rozmin@bolton.ac.uk', 'telephone':'765478239878','firstname': 'Rozmin', 'lastname': 'Shaikh', 'middlename':'Rose', 'dob':date(1999,10,14), 'student_no': '2228266'},
            {'username':'azma', 'email':'Azma@bolton.ac.uk', 'telephone':'78124342433','firstname': 'Azma', 'lastname': 'Azzy', 'middlename':'Jane',  'dob':date(1995,8,15),'student_no': '2233847'},
            {'username':'amar', 'email':'amar@bolton.ac.uk', 'telephone':'78942409599','firstname': 'Amar', 'lastname': 'Amarrii','middlename':'Hakim',  'dob':date(1999,9,3),'student_no': '22993883'},
            {'username':'christian', 'email':'christian@bolton.ac.uk', 'telephone':'781625489533','firstname': 'Christian', 'lastname': 'Okeke', 'middlename':'Samuel','dob':date(1995,10,14), 'student_no': '22674663'},
            {'username':'nalu', 'email':'nalu@bolton.ac.uk', 'telephone':'78120984523','firstname': 'Chukwunalu', 'lastname': 'Obi', 'middlename':'Prosper', 'dob':date(1996,10,31), 'student_no': '22139844'}
            ]

course_data=[
    
    {'code':'SWE7101','name':'Contemporary Software Engineering','description': "This course includes modern software practices like Agile", 'course_level':7,'course_credit':140 },
    {'code':'SWE7102','name':'Advance Software Developement','description': "This course includes hard developement of software", 'course_level':7,'course_credit':140 }
    ]

def seed_data():
    for user_staff in user_staff_data:
        staff_user = User(username=user_staff['username'], email=user_staff['email'], telephone=user_staff['telephone'], password=user_password, is_staff=True)

        db.session.add(staff_user)
        db.session.commit()

        staff = Staff(first_name=user_staff['firstname'], last_name=user_staff['lastname'], staff_code=user_staff['staffcode'], user_id=staff_user.id)
        db.session.add(staff)
        db.session.commit()

    for user_student in user_student_data:
        student_user=User(username=user_student['username'],email=user_student['email'],telephone=user_student['telephone'],password=user_password,is_student=True)
        db.session.add(student_user)
        db.session.commit()

        student=Student(first_name=user_student['firstname'], last_name=user_student['lastname'],middle_name=user_student['middlename'], student_no=user_student['student_no'],date_of_birth=user_student['dob'], is_active=True, user_id=student_user.id)
        db.session.add(student)
        db.session.commit()

    for course in course_data:
        course=Course(course_name=course['name'],course_code=course['code'],course_description=course['description'], course_level=course['level'], course_credit=['credit'])
        db.session.add(course)
        db.session.commit()
