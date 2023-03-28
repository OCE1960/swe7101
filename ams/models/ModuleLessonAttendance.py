from sqlalchemy import Identity
from .. import db
from .. import ma

class ModuleLessonAttendance(db.Model):
    __tablename__ = 'module_lesson_attendances'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    module_lesson_id = db.Column(db.Integer, db.ForeignKey('module_lessons.id'), nullable=False)
    attendance_status = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=True)
    
    
    def __repr__(self) -> str:
       return f"ModuleLessonAttendance(id={self.id!r}, student_id{self.student_id!r}, module_lesson_id{self.module_lesson_id!r}, attendance_status{self.attendance_status!r})"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class ModuleLessonAttendanceSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "student_id", "module_lesson_id", "attendance_status", "updated_by")


module_lesson_attendance_schema = ModuleLessonAttendanceSchema()
module_lesson_attendances_schema = ModuleLessonAttendanceSchema(many=True)