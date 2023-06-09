from sqlalchemy import Identity
from .. import db
from .. import ma

class Semester(db.Model):
    __tablename__ = 'semesters'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True, index=True)
    session = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.String(5), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    module_enrollments = db.relationship('ModuleEnrollment', backref='semesters')
    module_lessons = db.relationship('ModuleLesson', backref='semesters')
    
    def __repr__(self) -> str:
       return f"Semester(id={self.id!r}, session{self.session!r}, year={self.year!r}, is_active={self.last_name!r})"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class SemesterSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "session", "year", "is_active")


semester_schema = SemesterSchema()
semesters_schema = SemesterSchema(many=True)