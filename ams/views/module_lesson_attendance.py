from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from ..models.ModuleLesson import ModuleLesson
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.ModuleLessonAttendance import ModuleLessonAttendance
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

        if module:
            for student in student_list:
                student_instance = Student.query.get_or_404(student["id"])
                module_lesson_attendance =ModuleLessonAttendance(student_id=student_instance.id, module_lesson_id=module_lesson_id, attendance_status=student["attendance_status"], updated_by=staff.id)
                module_lesson_attendance.save()
            return jsonify({"msg": "Attendance Registration Successful"}),HTTPStatus.CREATED
        else:
            return jsonify({"msg": "Staff not assigned to this module"}),HTTPStatus.UNAUTHORIZED


    except Exception as e:
        return jsonify({"error": "There was an error registering students"}), HTTPStatus.BAD_REQUEST
    
        




