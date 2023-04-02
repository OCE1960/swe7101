import random
import string

from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, jwt
from ..models.ModuleLesson import ModuleLesson
from ..models.Module import Module
from ..models.Semester import Semester
from ..models.Student import Student,students_schema
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.User import User
from http import HTTPStatus



bp = Blueprint('module-lessons', __name__, url_prefix='/api/v1/module-lessons')
    
@bp.route("/<id>", methods=["POST"])
@jwt_required()
def generate_checkin_code(id):
    try:
        user_name = get_jwt_identity()
        db.session.execute(db.select(User).where(User.username == user_name).where(User.is_staff == True)).scalar_one()
        module_lesson = db.session.execute(db.select(ModuleLesson).filter_by(id=id)).scalar_one()
        letters = string.ascii_uppercase
        checking_code = ''.join(random.choice(letters) for i in range(6))
        module_lesson.checking_code = checking_code
        db.session.commit()
        return jsonify({"code": checking_code}), 200
    except Exception as e:
        return jsonify({"error": "Their was an Error Generating the Checking Code"}), 401
    


@bp.route("/students/<int:module_lesson_id>", methods=["GET"])
@jwt_required()
def module_lesson_students(module_lesson_id):
    try:
        user_name = get_jwt_identity()
        db.session.execute(db.select(User).where(User.username == user_name).where(User.is_staff == True)).scalar_one()
        module_lesson = db.session.execute(db.select(ModuleLesson).filter_by(id=module_lesson_id)).scalar_one()
        
        module_enrollment = ModuleEnrollment.query.filter_by(module_id=module_lesson.module_id, semester_id=module_lesson.semester_id)

        student_list =[]
        for module_student in module_enrollment:
            students = Student.query.get_or_404(module_student.student_id)
            student_list.append(students)

        response = {
            "number_of_students" : len(student_list),
            "students": students_schema.dump(student_list)
        }
        
        return jsonify(response), HTTPStatus.OK

    except Exception as e:
        return jsonify({"error": "There was an issue fetching students for this lesson"}), HTTPStatus.BAD_REQUEST



@bp.route("/<int:module_lesson_id>/", methods=["PUT"])
@jwt_required()
def update_module_lesson(module_lesson_id):
    try:
        user_name = get_jwt_identity()
        db.session.execute(db.select(User).where(User.username == user_name).where(User.is_staff == True)).scalar_one()

        module_lesson = db.session.execute(db.select(ModuleLesson).where(ModuleLesson.id == module_lesson_id)).scalar_one()
        module = db.session.execute(db.select(Module).where(Module.id == module_lesson.module_id)).scalar_one()
        semester = db.session.execute(db.select(Semester).where(Semester.id == module.semester_id)).scalar_one()
        
        if semester.is_active:
            module_id = request.json.get('module_id')
            venue = request.json.get('venue')
            date = request.json.get('date')
            time = request.json.get('time')
            semester_id = request.json.get('semester)id')

            return jsonify({"success": "Okay"}), 200
        
        else:
            return jsonify({"error": "Changes for previous semester cannot be made"}), 401
        
    except Exception as e:
        return jsonify(str(e)), 401