from sqlalchemy import Identity
from .. import db
from .. import ma

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    middle_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    student_no = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    module_enrollments = db.relationship('ModuleEnrollment', backref='students')
    module_lesson_attendance = db.relationship('ModuleLessonAttendance', backref='students')
    
    def __repr__(self) -> str:
       return f"Student(id={self.id!r}, first_name{self.first_name!r}, middle_name={self.middle_name!r}, last_name={self.last_name!r})"
    
class StudentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "first_name", "middle_name", "last_name", "student_no", "date_of_birth", "user_id","_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("student_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("students"),
        }
    )


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)