from .. import db
from ..models.User import User
from ..models.Staff import Staff
from ..models.Student import Student
from ..models.Course import Course


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

    db.session.add_all()
    db.session.add_all([staff1])
    db.session.commit()