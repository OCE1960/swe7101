from sqlalchemy import Identity
from .. import db
from .. import ma

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    course_code = db.Column(db.String(80), nullable=False, unique=True)
    course_name = db.Column(db.String(150), nullable=False)
    course_description = db.Column(db.Text, nullable=False)
    course_level = db.Column(db.Integer, nullable=False)
    course_credit = db.Column(db.Integer, nullable=False)
    modules = db.relationship('Module', backref='courses')

    
    
    def __repr__(self) -> str:
       return f"Course(id={self.id!r}, course_code{self.course_code!r}, course_name={self.course_name!r})"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class CourseSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "course_code", "course_name", "course_description", "course_level", "course_credit", "_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("course_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("courses"),
        }
    )


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)