from sqlalchemy import Identity
from .. import db
from .. import ma
from . import Staff

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    module_code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    module_enrollments = db.relationship('ModuleEnrollment', backref='modules')
    module_lessons = db.relationship('ModuleLesson', backref='modules')
    
    
    def __repr__(self) -> str:
       return f"Module(id={self.id!r}, name{self.name!r}, module_code={self.module_code!r})"
    
class ModuleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "module_code", "description", "staff_id", "semester_id", "_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("module_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("modules"),
        }
    )


module_schema = ModuleSchema()
modules_schema = ModuleSchema(many=True)