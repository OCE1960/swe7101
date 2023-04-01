from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from .. import db
from ..models.ModuleLesson import ModuleLesson
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.ModuleLessonAttendance import ModuleLessonAttendance, module_lesson_attendances_schema
from ..models.Module import Module
from ..models.Student import Student
from ..models.Staff import Staff
from ..models.User import User
from http import HTTPStatus


bp = Blueprint('module-lessons-attendance', __name__, url_prefix='/api/v1/module-lessons-attendance')


@bp.route("/<int:module_lesson_id>", methods=["POST"])
@jwt_required()
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
def update_module_lesson_attendance(module_lesson_id, student_id):
    try:
        attendance = db.session.execute(db.select(ModuleLessonAttendance).where(ModuleLessonAttendance.module_lesson_id == module_lesson_id).where(ModuleLessonAttendance.student_id == student_id)).scalar_one()
        status = request.json.get("status", None)
        valid_status_codes = ["P", "A", "O", "N", "C"]
        if status not in valid_status_codes:
            return jsonify({"invalid": "Invalid Status Code"}), 401
        
        attendance.attendance_status = status
        db.session.commit()
        
        return jsonify({"success": "Attendance Updated Successfully"}), 200
        
    except Exception as e:
        return jsonify(str(e)), 401



