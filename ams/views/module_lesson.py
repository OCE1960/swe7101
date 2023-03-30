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
from ..models.User import User


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

    