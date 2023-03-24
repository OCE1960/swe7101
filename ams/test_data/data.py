from .. import db
from ..models.User import User
from ..models.Staff import Staff
from ..models.Student import Student
from ..models.Course import Course
from ..models.Semester import Semester
from ..models.Module import Module
from werkzeug.security import generate_password_hash, check_password_hash

def seed_data():
    password = 'password'
    
    user_password = generate_password_hash(password, 'sha256')   
    user1 = User(username='francis', email='francis@bolton.ac.uk', telephone='78124523', password='password', is_staff=True)
    user2 = User(username='ibtisam', email='ibtisam@bolton.ac.uk', telephone='78124524', password='password', is_staff=True)
    
    staff1 = Staff(first_name='Francis', last_name='Morris', staff_code='7813', users=user1)
    staff2=Staff(first_name='Ibtisam',last_name='Mogul', staff_code="7814",users=user2)

    user3=User(username='rozmin',email='rozmin@bolton.ac.uk',telephone='7654789878',password='password',is_student=True)
    student1=Student(first_name='Rozmin', last_name='Shaikh', student_no='2228266', users=user3)

    course1=Course(code=123,course_name="Masters in Software Engineering",course_description="This is the Masters course for Software engineering", course_level=7, course_credit=140)
    
    semester1=Semester(session=1, year=1, is_Active=True)
    
    module1=Module(name="Contemporary Software Practices", module_code="SWE7101", description="First Module of Msc in Software Engineering")
    
    moduleLesson1=moduleLesson1(venue="Richie Computing Lab", time="9:00", date="12-02-2023", checking_code="AHB123")

    moduleLessonAttendance1=moduleLessonAttendance1(attendance_status="Present")
    db.session.add_all([staff1])
    db.session.commit()