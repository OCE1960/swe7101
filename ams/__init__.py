from flask import Flask 
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import click
from flask.cli import with_appcontext


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
    
    
    from .views import user
    from .views import module_lesson
    app.register_blueprint(module_lesson.bp)
    app.register_blueprint(user.bp)
    
    
    with app.app_context():
        db.create_all()
              
    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    #this adds the custom command to app
    app.cli.add_command(seed_data)

    return app




"""
A custom command for seeding database test data
to execute type : flask --app ams seed_data    in the terminal

"""
@click.command(name='seed_data')
@with_appcontext
def seed_data():
    from .test_data import data
    db.drop_all() 
    db.create_all()
    data.seed_data() 





