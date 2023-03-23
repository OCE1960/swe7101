from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from ..models.User import User, user_schema


bp = Blueprint('auth', __name__, url_prefix='/auth')

# create_access_token() function is used to actually generate the JWT.
@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    try:
        user = db.session.execute(db.select(User).where(User.username == username)).scalar_one()
        userp = check_password_hash(user.password, password)
        if(userp):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token)
        return jsonify({"msg": "Bad username or password"}), 401 
    except Exception as e:
        return jsonify({"error": "Invalid Credential"}), 401

    