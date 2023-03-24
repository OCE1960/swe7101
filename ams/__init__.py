from flask import Flask 
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()

jwt = JWTManager()

ma = Marshmallow() 

def create_app():
    app = Flask(__name__)

    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/project.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = "secret"
    
    
   
    db.init_app(app)
    
    ma.init_app(app)
    
    jwt.init_app(app)
    
    
    from .models import Course
    from .models import Module
    from .models import ModuleEnrollment
    from .models import ModuleLesson
    from .models import ModuleLessonAttendance
    from .models import Semester
    from .models import Staff
    from .models import Student
    from .models import User
    from .models import Module_Staff_M2M
    from .test_data import data
    
    from .views import user
    app.register_blueprint(user.bp)
    
    
    with app.app_context():
        db.drop_all() 
        db.create_all()
        data.seed_data()  
              
    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app