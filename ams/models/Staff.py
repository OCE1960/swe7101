from sqlalchemy import Identity
from .. import db
from .. import ma

class Staff(db.Model):
    __tablename__ = 'staffs'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    middle_name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(20), unique=True, nullable=False)
    staff_code = db.Column(db.String(120), nullable=False)
    rank = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendances_marked = db.relationship('ModuleLessonAttendance', backref='staffs')
    
    def __repr__(self) -> str:
       return f"Staff(id={self.id!r}, first_name{self.first_name!r}, middle_name={self.middle_name!r}, last_name={self.last_name!r})"
    
class StaffSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "first_name", "middle_name", "last_name", "staff_code", "rank", "title", "user_id","_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("staff_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("staffs"),
        }
    )


staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)