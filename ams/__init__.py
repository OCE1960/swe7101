from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()

ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/project.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   
    db.init_app(app) 
    
    from .models import Module
    from .models import ModuleEnrollment
    from .models import ModuleLesson
    from .models import ModuleLessonAttendance
    from .models import Semester
    from .models import Staff
    from .models import Student
    from .models import User   

    with app.app_context():
        #db.drop_all() #Function to Delete the entire Table
        db.create_all()
        
    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app