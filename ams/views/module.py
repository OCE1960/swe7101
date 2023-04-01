import random
import string
from datetime import date

from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from .. import db, jwt
from ..models.ModuleLesson import ModuleLesson, module_lessons_schema
from ..models.Module import Module
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.User import User


bp = Blueprint('modules', __name__, url_prefix='/api/v1/modules')
    
@bp.route("/<int:module_id>", methods=["GET"])
@jwt_required()
def get_module_lessons(module_id):
    try:
        db.session.execute(db.select(Module).filter_by(id=module_id)).scalar_one()
        user_name = get_jwt_identity()
        user = db.session.execute(db.select(User).where(User.username == user_name)).scalar_one()
        if user.is_student:
            db.session.execute(db.select(ModuleEnrollment).filter_by(module_id=module_id, student_id=user.id)).scalar_one()
        today = date.today()
        module_lessons = db.session.execute(db.select(ModuleLesson).where(ModuleLesson.module_id == module_id).where(ModuleLesson.date <= today)).scalars()
        context = {
            "success" : True,
            "data" : module_lessons_schema.dump(module_lessons)
        }
        return jsonify(context)
    except Exception as e:
        return jsonify({"error": "Their was an Error fetching the Module Lesson"}), 401
    
    
@bp.route("/lessons", methods=["GET"])
@jwt_required()
def generate_assigned_lessons(id):
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

    