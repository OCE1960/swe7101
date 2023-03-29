from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, time

from .. import db
from ..models.User import User
from ..models.Staff import Staff
from ..models.Student import Student
from ..models.Course import Course
from ..models.Semester import Semester
from ..models.Module import Module
from ..models.ModuleLesson import ModuleLesson
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.ModuleLessonAttendance import ModuleLessonAttendance

password = 'password'
user_password = generate_password_hash(password, 'sha256') 

user_staff_data =[{'username':'francis', 'email':'francis@bolton.ac.uk', 'telephone':'7812458923', 'firstname': 'Francis', 'lastname': 'Morris', 'staffcode': '7813'},
            {'username':'ibtiiisam', 'email':'ibtisam@bolton.ac.uk', 'telephone':'7812452544','firstname': 'Ibtiisam', 'lastname': 'Mogul', 'staffcode': '7814'}, 
                {'username':'celestine', 'email':'celestine@bolton.ac.uk', 'telephone':'7812223544','firstname': 'Celestine', 'lastname': 'Oba', 'staffcode': '7815'},
                {'username':'stella', 'email':'stella@bolton.ac.uk', 'telephone':'7811252544','firstname': 'Stella', 'lastname': 'Karine', 'staffcode': '7816'},
                {'username':'alvin', 'email':'alvin@bolton.ac.uk', 'telephone':'7810099544','firstname': 'Alvin', 'lastname': 'Peters', 'staffcode': '7817'},
            ]

user_student_data =[
            {'username':'rozmin', 'email':'rozmin@bolton.ac.uk', 'telephone':'765478239878','firstname': 'Rozmin', 'lastname': 'Shaikh', 'middlename':'Rose', 'dob':date(1999,10,14), 'student_no': '2228266'},
            {'username':'azma', 'email':'Azma@bolton.ac.uk', 'telephone':'78124342433','firstname': 'Azma', 'lastname': 'Azzy', 'middlename':'Jane',  'dob':date(1995,8,15),'student_no': '2233847'},
            {'username':'amar', 'email':'amar@bolton.ac.uk', 'telephone':'78942409599','firstname': 'Amar', 'lastname': 'Amarrii','middlename':'Hakim',  'dob':date(1999,9,3),'student_no': '22993883'},
            {'username':'christian', 'email':'christian@bolton.ac.uk', 'telephone':'781625489533','firstname': 'Christian', 'lastname': 'Okeke', 'middlename':'Samuel','dob':date(1995,10,14), 'student_no': '22674663'},
            {'username':'nalu', 'email':'nalu@bolton.ac.uk', 'telephone':'78120984523','firstname': 'Chukwunalu', 'lastname': 'Obi', 'middlename':'Prosper', 'dob':date(1996,10,31), 'student_no': '22139844'}
            ]



course_seed_data=[
    {'name':'Software Engineering', 'courseCode':'SWE','description':'The Software Engineering course syllabus is designed to impart knowledge about Computer Programming, Web Development, Data Structures, Project Management, etc','courseLevel': 700, 'courseCredit':180},
    {'name':'Cloud and Network Security', 'courseCode':'CIS','description':'The course introduces tools and tactics to manage cybersecurity risks, identify various types of common threats, evaluate the organization security','courseLevel': 700, 'courseCredit':150},
    {'name':'Data Analytics and Technologies', 'courseCode':'DAT','description':'You will learn about the various statistical and analytical tools and techniques you can use in order to gain a deeper understanding of your data','courseLevel': 700, 'courseCredit':120},
    {'name':'Supply Chain Management', 'courseCode':'SCM','description':' This focuses on the movement and storage of materials, data, inventory, goods and finances as they move from the point of origin to the point of purchase.','courseLevel': 700, 'courseCredit':100},
    {'name':'Civil Engineering', 'courseCode':'CVE','description':'deals with the design, construction and maintenance of our built environment, from buildings to bridges, roads to railways','courseLevel': 700, 'courseCredit':100}

]

module_seed_data=[
        {'seeder_id':1, 'semester_id':1,'moduleCode':'SWE7101', 'name': 'Contemporary Software Engineering Practices', 'description': 'There are two ways of constructing a software design....'},
        {'seeder_id':1,'semester_id':2,'moduleCode':'SWE7102', 'name': 'Advanced Software Development', 'description': 'The advance method of constructing a software design....'},
        {'seeder_id':1,'semester_id':1,'moduleCode':'SWE7103', 'name': 'Research Methods', 'description': 'Deals with the various ways of carrying out research....'},
        {'seeder_id':1,'semester_id':2,'moduleCode':'SWE7104', 'name': 'Devops', 'description': 'Deals with the combination of software development (dev) and operations (ops)....'},

        {'seeder_id':2,'semester_id':1,'moduleCode':'CIS7101', 'name': 'Advanced Cloud Penetration Testing and Forensics', 'description': 'The testing and security of cloud systems'},
        {'seeder_id':2,'semester_id':2,'moduleCode':'CIS7102', 'name': 'Global Infrastructure', 'description': 'The in depth knowledge of global infra....'},
        {'seeder_id':2,'semester_id':1,'moduleCode':'CIS7103', 'name': 'Research Methods', 'description': 'Deals with the various ways of carrying out research....'},
        {'seeder_id':2,'semester_id':2,'moduleCode':'CIS7104', 'name': 'Devops', 'description': 'Deals with the combination of software development (dev) and operations (ops)....'},


        {'seeder_id':3,'semester_id':1,'moduleCode':'DAT7101', 'name': 'Data Science', 'description': 'Deals with the science of data manipulation.'},
        {'seeder_id':3,'semester_id':2,'moduleCode':'DAT7102', 'name': 'Big Data Technologies', 'description': 'Manage big data for complex industries'},
        {'seeder_id':3,'semester_id':1,'moduleCode':'DAT7103', 'name': 'Research Methods', 'description': 'Deals with the various ways of carrying out research....'},
        {'seeder_id':3,'semester_id':2,'moduleCode':'DAT7104', 'name': 'Solutions Design and Ethical Practice', 'description': 'Deals with the crestion of designs ethically'},


        {'seeder_id':4,'semester_id':1,'moduleCode':'SCM7101', 'name': 'Logistics Management', 'description': 'This deals with logistic management'},
        {'seeder_id':4,'semester_id':2,'moduleCode':'SCM7102', 'name': 'Supply Chain Strategy', 'description': 'This deals with strategies involved in supply chain'},
        {'seeder_id':4,'semester_id':1,'moduleCode':'SCM7103', 'name': 'Research Methods', 'description': 'Deals with the various ways of carrying out research....'},
        {'seeder_id':4,'semester_id':2,'moduleCode':'SCM7104', 'name': 'Finance and Decision Making', 'description': 'This deals with ways to manage finance'},

        {'seeder_id':5,'semester_id':1,'moduleCode':'CVE7101', 'name': 'Advanced Geotechnical Modelling, Analysis and Design', 'description': 'This deals with the geographical design and model of....'},
        {'seeder_id':5,'semester_id':2,'moduleCode':'CVE7102', 'name': 'Advanced Structural Modelling, Analysis and Design', 'description': 'The advance method of structuring buildings....'},
        {'seeder_id':5,'semester_id':1,'moduleCode':'CVE7103', 'name': 'English for Engineering', 'description': 'Deals with the write up of report'},
        {'seeder_id':5,'semester_id':2,'moduleCode':'CVE7104', 'name': 'Project Management', 'description': 'Deals with the advance methods of managing projects'}

]

semester_seed_data=[
    {'session': 'Fall', 'year': '2015/2016', 'isActive':False},
    {'session': 'Spring', 'year': '2016/2017', 'isActive':False},
    {'session': 'Antumn', 'year': '2017/2018', 'isActive':False},
    {'session': 'Winter', 'year': '2018/2019', 'isActive':False},
    {'session': 'Harmattan', 'year': '2019/2020', 'isActive':False},
    {'session': 'Cold', 'year': '2020/2021', 'isActive':False},
    {'session': 'Summer', 'year': '2021/2022', 'isActive':False},
    {'session': 'RAYSS', 'year': '2022/2023', 'isActive':True},
    {'session': 'fALLLSS', 'year': '2023/2024', 'isActive':False},

]

module_lesson_seed_data=[
    {'module_id':1, 'venue': "Barnee Lab", 'date': date(2023,4,11), 'time':time(6,47)},
    {'module_id':1,'venue': "Barnee Lab", 'date': date(2023,4,12), 'time':time(6,47)},
    {'module_id':1,'venue': "Barnee Lab", 'date': date(2023,4,13), 'time':time(6,47)},
    {'module_id':1,'venue': "Barnee Lab", 'date': date(2023,4,14), 'time':time(6,47)},

    {'module_id':1,'venue': "Sinclair Lab", 'date': date(2023,4,11), 'time':time(6,47)},
    {'module_id':1,'venue': "Sinclair Lab", 'date': date(2023,4,12), 'time':time(9,47)},
    {'module_id':1,'venue': "Sinclair Lab", 'date': date(2023,4,13), 'time':time(9,47)},
    {'module_id':1,'venue': "Sinclair Lab", 'date': date(2023,4,14), 'time':time(9,47)},

    {'module_id':1,'venue': "Van Neumann Lab", 'date': date(2023,4,11), 'time':time(12,47)},
    {'module_id':1,'venue': "Van Neumann Lab", 'date': date(2023,4,12), 'time':time(12,47)},
    {'module_id':2,'venue': "Van Neumann Lab", 'date': date(2023,4,13), 'time':time(12,47)},
    {'module_id':2,'venue': "Van Neumann Lab", 'date': date(2023,4,14), 'time':time(12,47)},

    {'module_id':2,'venue': "Albert Einstein Lab", 'date': date(2023,4,11), 'time':time(15,47)},
    {'module_id':2,'venue': "Albert Einstein Lab", 'date': date(2023,4,12), 'time':time(15,47)},
    {'module_id':2,'venue': "Albert Einstein Lab", 'date': date(2023,4,13), 'time':time(15,47)},
    {'module_id':2,'venue': "Albert Einstein Lab", 'date': date(2023,4,14), 'time':time(15,47)},

    {'module_id':2,'venue': "Newton Lab", 'date': date(2023,4,11), 'time':time(18,47)},
    {'module_id':2,'venue': "Newton Lab", 'date': date(2023,4,12), 'time':time(18,47)},
    {'module_id':2,'venue': "Newton Lab", 'date': date(2023,4,13), 'time':time(18,47)},
    {'module_id':2,'venue': "Newton Lab", 'date': date(2023,4,14), 'time':time(18,47)},

]

module_enrollment_seed_data=[
    {''}
]

module_lesson_attendance_seed_data=[
    {'attendance_status' : 'Present'},{'attendance_status' : 'Absent'},{'attendance_status' : 'Notified Absent'},{'attendance_status' : 'International'}
]








def seed_data():  
    

    for user_staff in user_staff_data:
       
        staff_user = User(username=user_staff['username'], email=user_staff['email'], telephone=user_staff['telephone'], password=user_password, is_staff=True, is_active=True)
        staff_user.save()
        

        staff = Staff(first_name=user_staff['firstname'], last_name=user_staff['lastname'], staff_code=user_staff['staffcode'], user_id=staff_user.id)
        staff.save()
        
        
    for user_student in user_student_data:
        student_user=User(username=user_student['username'],email=user_student['email'],telephone=user_student['telephone'],password=user_password,is_student=True, is_active=True)
        student_user.save()
        

        student=Student(first_name=user_student['firstname'], last_name=user_student['lastname'],middle_name=user_student['middlename'], student_no=user_student['student_no'],date_of_birth=user_student['dob'], user_id=student_user.id)
        student.save()
        


    for courses in course_seed_data:

        course = Course(course_code=courses['courseCode'], course_name=courses['name'],course_description=courses['description'], course_level=courses['courseLevel'], course_credit=courses['courseCredit'])
        course.save()
        
    
    for semesters in semester_seed_data:

        semester = Semester(session=semesters['session'], year=semesters['year'], is_active=semesters['isActive'])
        semester.save()
        

    get_semester1 = Semester.query.filter_by(id=8).first()
    get_semester2 = Semester.query.filter_by(id=9).first()
    
    get_course1 = Course.query.filter_by(id=1).first()
    get_course2 = Course.query.filter_by(id=2).first()
    get_course3 = Course.query.filter_by(id=3).first()
    get_course4 = Course.query.filter_by(id=4).first()
    get_course5 = Course.query.filter_by(id=5).first()

    for modules in module_seed_data:
        if modules['seeder_id'] ==1:
            if modules['semester_id']==1:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester1.id, course_id=get_course1.id)
                module.save()
                
            else:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester2.id, course_id=get_course1.id)
                module.save()
                

        if modules['seeder_id'] ==2:
            if modules['semester_id']==1:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester1.id, course_id=get_course2.id)
                module.save()
                
            else:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester2.id, course_id=get_course2.id)
                module.save()
               

        if modules['seeder_id'] ==3:
            if modules['semester_id']==1:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester1.id, course_id=get_course3.id)
                module.save()
                
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester2.id, course_id=get_course3.id)
                module.save()
                

        if modules['seeder_id'] ==4:
            if modules['semester_id']==1:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester1.id, course_id=get_course4.id)
                module.save()
                
            else:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester2.id, course_id=get_course4.id)
                module.save()
                

        if modules['seeder_id'] ==5:
            if modules['semester_id']==1:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester1.id, course_id=get_course5.id)
                module.save()
              
            else:
                module = Module(name=modules['name'], module_code=modules['moduleCode'], description=modules['description'], semester_id=get_semester2.id, course_id=get_course5.id)
                module.save()
                

        module1= Module.query.filter_by(id=1).first()
        module2 = Module.query.filter_by(id=2).first()   



    """
    seeder that seeds data for module lessons
    """

    for lessons in module_lesson_seed_data:
        if lessons['module_id'] ==1:
            module_lesson = ModuleLesson(venue=lessons['venue'], date=lessons['date'], time=lessons['time'], module_id=module1.id, semester_id=get_semester1.id)
            module_lesson.save()
            
        if lessons['module_id'] ==2:
            module_lesson = ModuleLesson(venue=lessons['venue'], date=lessons['date'], time=lessons['time'], module_id=module2.id, semester_id=get_semester1.id)
            module_lesson.save()
            


    students = Student.query.all()
    moduless=Module.query.all()
    staffss = Staff.query.all()

    """
    seeder that seeds data for module enrollment
    """
    for mod in moduless:
        for student in students:
            enrollModule = ModuleEnrollment(module_id=mod.id,student_id=student.id,semester_id=get_semester1.id)
            enrollModule.save()
            

    """
    seeder that seeds data for the many to many relationship between module and staff
    """
    for mod_staff in moduless:
        for staff_mod in staffss:
            staaff = Staff.query.filter_by(id=staff_mod.id).first()
            moodule = Module.query.filter_by(id=mod_staff.id).first()
            moodule.module_staff.append(staaff)
            db.session.commit()
    
    module_lessn = ModuleLesson.query.all()[:10]
    for modul in module_lessn:
        for sttud in students:
            if sttud.id %2==0:
                moduleLessonAttendance = ModuleLessonAttendance(student_id=sttud.id, module_lesson_id=modul.id, attendance_status='Present')
                moduleLessonAttendance.save()
                
            else:
                moduleLessonAttendance = ModuleLessonAttendance(student_id=sttud.id, module_lesson_id=modul.id, attendance_status='Absent')
                moduleLessonAttendance.save()
                
            




       


  


    