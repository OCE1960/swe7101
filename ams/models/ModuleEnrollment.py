from sqlalchemy import Identity
from .. import db
from .. import ma

class ModuleEnrollment(db.Model):
    __tablename__ = 'module_enrollments'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    
    
    def __repr__(self) -> str:
       return f"ModuleEnrollment(id={self.id!r}, module_id{self.module_id!r})"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class ModuleEnrollmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "module_id", "student_id", "semester_id")

module_enrollment_schema = ModuleEnrollmentSchema()
module_enrollments_schema = ModuleEnrollmentSchema(many=True)