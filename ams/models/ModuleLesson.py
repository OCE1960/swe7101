from sqlalchemy import Identity
from .. import db
from .. import ma

class ModuleLesson(db.Model):
    __tablename__ = 'module_lessons'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    venue = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    checking_code = db.Column(db.String(80), nullable=True)
    module_lesson_attendance = db.relationship('ModuleLessonAttendance', backref='module_lessons')
    
    
    def __repr__(self) -> str:
       return f"ModuleLesson(id={self.id!r}, venue{self.venue!r}, module_id{self.module_id!r}, semester_id{self.semester_id!r})"
    
class ModuleLessonSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "module_id", "venue", "semester_id", "date", "time", "checking_code")


module_lesson_schema = ModuleLessonSchema()
module_lessons_schema = ModuleLessonSchema(many=True)