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
from ..models.Module import Module, modules_schema
from ..models.ModuleEnrollment import ModuleEnrollment
from ..models.User import User
from ..models.Staff import Staff, staffs_schema
from ..models.Semester import Semester




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
    
@bp.route("/<int:module_id>/semester", methods=["GET"])
@jwt_required()
def get_module_currrent_semester_lessons(module_id):
    try:
        db.session.execute(db.select(Module).filter_by(id=module_id)).scalar_one()
        user_name = get_jwt_identity()
        user = db.session.execute(db.select(User).where(User.username == user_name)).scalar_one()
        if user.is_student:
            db.session.execute(db.select(ModuleEnrollment).filter_by(module_id=module_id, student_id=user.id)).scalar_one()

        semester = db.session.execute(db.select(Semester).where(Semester.is_active == True)).scalar_one()

        module_lessons = db.session.execute(db.select(ModuleLesson).filter_by(module_id = module_id, semester_id = semester.id )).scalars()
        context = {
            "success" : True,
            "data" : module_lessons_schema.dump(module_lessons)
        }
        return jsonify(context), 200
    except Exception as e:
        return jsonify({"error": "No Semester not active"}), 401
    
    
@bp.route("/lessons", methods=["GET"])
@jwt_required()
def get_staff_lessons():
    try:
        user_name = get_jwt_identity()
        user = db.session.execute(db.select(User).where(User.username == user_name).where(User.is_staff == True)).scalar_one()
        staff = db.session.execute(db.select(Staff).where(Staff.user_id == user.id)).scalar_one()
        assigned_modules = staff.modules
        lessons = []
        for module in assigned_modules:
            
            lesson = {
                "module_id" : module.id,
                "lessons" : module_lessons_schema.dump(module.module_lessons)
            }
            
            lessons.append(lesson)
        
        context_response = {
            "data" : lessons,
            "success" : True,
        }
            
        return jsonify(context_response), 200

    except Exception as e:
        return jsonify({"error": "Their was an There was an error fetching your lessons"}), 401
    



    