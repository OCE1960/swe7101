from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import unset_jwt_cookies
from werkzeug.security import check_password_hash

from .. import db
from ..models.User import User, user_schema, users_schema

from flasgger import swag_from


bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# create_access_token() function is used to actually generate the JWT.
@bp.route("/login", methods=["POST"])
@swag_from("../../docs/auth/login.yaml")
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
            return jsonify(context), 200
        return jsonify({"error": "Bad username or password"}), 401 
    except Exception as e:
        return jsonify({"error": "Invalid Credential"}), 401
    
@bp.route("/users/<id>", methods=["GET"])
@jwt_required()
@swag_from("../../docs/auth/user.yaml")
def user_detail(id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
        return user_schema.dump(user)
    except Exception as e:
        return jsonify(e.__repr__()), 401
    
    
@bp.route("/users", methods=["GET"])
@jwt_required()
@swag_from("../../docs/auth/users_list.yaml")
def users():
    try:
        users = db.session.execute(db.select(User).order_by(User.username)).scalars()
        return users_schema.dump(users) 
    except Exception as e:
        return jsonify(e.__repr__()), 401
    
@bp.route("/logout", methods=["POST"])
@swag_from("../../docs/auth/logout.yaml")
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

    