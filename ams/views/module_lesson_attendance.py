from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from sqlalchemy import or_

from .. import db
from ..models.ModuleLesson import ModuleLesson, module_lesson_details_schema
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.ModuleLessonAttendance import ModuleLessonAttendance, module_lesson_attendances_schema
from ..models.Module import Module
from ..models.Semester import Semester
from ..models.Student import Student
from ..models.Staff import Staff
from ..models.User import User
from http import HTTPStatus
from flasgger import Swagger, swag_from

bp = Blueprint('module-lessons-attendance', __name__, url_prefix='/api/v1/module-lessons-attendance')


@bp.route("/<int:module_lesson_id>", methods=["POST"])
@jwt_required()
@swag_from("../../docs/attendance/student_self_attendance_registration.yaml")
def student_self_attendance_registration(module_lesson_id ):
    try:
        student_identity = get_jwt_identity()
        checkin_code = request.json.get("checkin_code", None)
        user = User.query.filter_by(username=student_identity).first()
        student = Student.query.filter_by(user_id=user.id).first()
        module_lesson = ModuleLesson.query.get_or_404(module_lesson_id)
       
        if checkin_code is not None:

            """
                Check if this particular student is enrolled for this particular module
            """
            module_enrollment = ModuleEnrollment.query.filter_by(module_id=module_lesson.module_id, student_id=student.id).first()
            if module_enrollment:
                """
                Validation of the checkin Code
                """
                if module_lesson.checking_code == checkin_code: 
                    moduleLesson_attendance = ModuleLessonAttendance(student_id=student.id, module_lesson_id=module_lesson.id, attendance_status='P')
                    moduleLesson_attendance.save()
                    return jsonify({"msg": "Attendance Registration Successful"}),HTTPStatus.CREATED
                else:
                    return jsonify({"error": "Invalid Checkin Code"}), HTTPStatus.NOT_ACCEPTABLE
            else:
                return jsonify({"error": "Student not enrolled"}), HTTPStatus.BAD_REQUEST
        else:
            return jsonify({"error": "Provide Checkin code"}), HTTPStatus.BAD_REQUEST
        
    except Exception as e:
        return jsonify({"error": "Something went wrong"}), HTTPStatus.UNAUTHORIZED
    

@bp.route("/staff/<int:module_lesson_id>", methods=["POST"])
@jwt_required()
@swag_from("../../docs/attendance/bulk_attendance_registration.yaml")
def bulk_attendance_registration(module_lesson_id ):
    try:
        staff_identity = get_jwt_identity()
        user = User.query.filter_by(username=staff_identity).first()
        staff = Staff.query.filter_by(user_id=user.id).first()
        module_lesson = ModuleLesson.query.get_or_404(module_lesson_id)
        
        module = Module.query.join(Staff.modules).filter(Staff.id == staff.id).filter_by(id=module_lesson.module_id).first()

        #a list of dictionaries containing student id and attendance status
        student_list = request.json.get('student_list', [])

        attendance_status_codes = ["P", "A", "O", "N", "C"]
        code_to_check = []

        for code in student_list:
            code_to_check.append(code["attendance_status"].upper())


        if set(code_to_check).issubset(attendance_status_codes):
            
            if module:
                for student in student_list:
                    student_instance = Student.query.get_or_404(student["id"])
                    module_lesson_attendance =ModuleLessonAttendance(student_id=student_instance.id, module_lesson_id=module_lesson_id, attendance_status=student["attendance_status"], updated_by=staff.id)
                    module_lesson_attendance.save()
                return jsonify({"msg": "Attendance Registration Successful"}),HTTPStatus.CREATED
            else:
                return jsonify({"msg": "Staff not assigned to this module"}),HTTPStatus.UNAUTHORIZED

        else:
             return jsonify({"msg": "Code not allowed"}),HTTPStatus.UNAUTHORIZED


    except Exception as e:
        return jsonify({"error": "There was an error registering students"}), HTTPStatus.BAD_REQUEST
    
        

@bp.route("/<int:module_lesson_id>", methods=["GET"])
@jwt_required()
@swag_from("../../docs/attendance/get_module_lesson_attendance.yaml")
def get_module_lesson_attendance(module_lesson_id):
    try:
        attendances = db.session.execute(db.select(ModuleLessonAttendance).filter_by(module_lesson_id=module_lesson_id)).scalars()
        attendance_records = []
        for attendance in attendances:
            student = db.session.execute(db.select(Student).where(Student.id == attendance.student_id)).scalar_one()
            user = db.session.execute(db.select(User).where(User.id == student.user_id)).scalar_one()
            full_name = student.first_name + " " + student.first_name
            record = {
                "student_id" : student.id,
                "username" : user.username,
                "email" : user.email,
                "name" : full_name,
                'attendance_status': attendance.attendance_status
            }

            attendance_records.append(record)
        context = {
            "success" : True,
            "data" : attendance_records
        }
        return jsonify(context)
    except Exception as e:
        return jsonify({"error": "No Attendance for this Lesson"}), 401
    
    
@bp.route("/<int:module_lesson_id>/students/<int:student_id>", methods=["PUT"])
@jwt_required()
@swag_from("../../docs/attendance/update_module_lesson_attendance.yaml")
def update_module_lesson_attendance(module_lesson_id, student_id):
    try:
        user_name = get_jwt_identity()
        db.session.execute(db.select(User).where(User.username == user_name).where(User.is_staff == True)).scalar_one()

        attendance = db.session.execute(db.select(ModuleLessonAttendance).where(ModuleLessonAttendance.module_lesson_id == module_lesson_id).where(ModuleLessonAttendance.student_id == student_id)).scalar_one()
        module_lesson = db.session.execute(db.select(ModuleLesson).where(ModuleLesson.id == attendance.module_lesson_id)).scalar_one()
        module = db.session.execute(db.select(Module).where(Module.id == module_lesson.module_id)).scalar_one()
        semester = db.session.execute(db.select(Semester).where(Semester.id == module.semester_id)).scalar_one()

        if semester.is_active:
            status = request.json.get("status", None)
            valid_status_codes = ["P", "A", "O", "N", "C"]
            if status not in valid_status_codes:
                return jsonify({"invalid": "Invalid Status Code"}), 401
            
            attendance.attendance_status = status
            db.session.commit()
            
            return jsonify({"success": "Attendance Updated Successfully"}), 200
        else:
            return jsonify({"msg": "Amendment prior to current semester not allowed"}), 401
        
    except Exception as e:
        return jsonify(str(e)), 401



@bp.route("/student-attendance", methods=["GET"])
@jwt_required()
@swag_from("../../docs/attendance/student_attendance_record.yaml")
def student_attendance_record():
    try:
        student_identity = get_jwt_identity()
        user = User.query.filter_by(username=student_identity).first()
        student = Student.query.filter_by(user_id=user.id).first()
        student_module = ModuleEnrollment.query.filter_by(student_id=student.id)
        student_module_list = []

        for module_id in student_module:
            student_module_list.append(module_id.module_id)

        module_lesson = db.session.query(ModuleLesson).filter(or_(ModuleLesson.module_id==student_module_list[0], ModuleLesson.module_id==student_module_list[1]))
        module_attendance = db.session.query(ModuleLessonAttendance).filter(ModuleLessonAttendance.student_id==student.id)

        module_lesson_id_list = []
        module_attendance_id_list = []

        for id in module_lesson:
            module_lesson_id_list.append(id.id)
        
        for id in module_attendance:
            module_attendance_id_list.append(id.module_lesson_id)
        

        data = []
        for id in module_lesson_id_list:
            module_lesson_details = db.session.query(ModuleLesson).filter(ModuleLesson.id==id).first()
            if id in module_attendance_id_list:
                
                attendance = {
                    "status" : "Present",
                    "summary" : "Checkin Validated",
                    "lesson" : module_lesson_details_schema.dump(module_lesson_details)
                }
                data.append(attendance)
            else:
                attendance = {
                    "status" : "Absent",
                    "summary" : "Checkin Not Validated",
                    "lesson_details" : module_lesson_details_schema.dump(module_lesson_details)
                }
                data.append(attendance)
        print(data)
        return jsonify(data), HTTPStatus.OK
        
    
    except Exception as e:
        return jsonify({"error": "Something went wrong"}), HTTPStatus.UNAUTHORIZED
