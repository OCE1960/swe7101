from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, jwt
from ..models.User import User, user_schema, users_schema


bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# create_access_token() function is used to actually generate the JWT.
@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    try:
        user = db.session.execute(db.select(User).where(User.username == username)).scalar_one()
        password_checked = check_password_hash(user.password, password)
        if(password_checked):
            access_token = create_access_token(identity=username)
            context = {
               "access_token" : access_token,
               "user_id" : user.id
            }
            return jsonify(context)
        return jsonify({"error": "Bad username or password"}), 401 
    except Exception as e:
        return jsonify({"error": "Invalid Credential"}), 401
    
@bp.route("/users/<id>", methods=["GET"])
@jwt_required()
def user_detail(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
        return user_schema.dump(user)
    except Exception as e:
        return jsonify(e.__repr__()), 401
    
@bp.route("/users", methods=["GET"])
@jwt_required()
def users():
    try:
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        return users_schema.dump(users) 
    except Exception as e:
        return jsonify(e.__repr__()), 401

    