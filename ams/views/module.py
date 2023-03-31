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

    