from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()

<<<<<<< HEAD
ma = Marshmallow()
=======
jwt = JWTManager()

ma = Marshmallow() 
>>>>>>> 9dac22e760932c03ceb9675d5e49d18e3c05fd35

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.root_path}/project.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
<<<<<<< HEAD
   
    db.init_app(app) 
=======
    
    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = "secret"
    
    
   
    db.init_app(app)
    
    ma.init_app(app)
    
    jwt.init_app(app)
    
>>>>>>> 9dac22e760932c03ceb9675d5e49d18e3c05fd35
    
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


    
    with app.app_context():
        db.drop_all() #Function to Delete the entire Table
        db.create_all()
<<<<<<< HEAD
        data.seed_data()
        
=======
        data.seed_data()  
              
>>>>>>> 9dac22e760932c03ceb9675d5e49d18e3c05fd35
    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app