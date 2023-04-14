from sqlalchemy import Identity
from .. import db
from .. import ma
from . import Module
from .Module_Staff_M2M import module_staff_m2m

class Staff(db.Model):
    __tablename__ = 'staffs'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True, index=True)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(20),  nullable=False)
    staff_code = db.Column(db.String(120), unique=True, nullable=False)
    rank = db.Column(db.String(120), nullable=True)
    title = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    
    def __repr__(self) -> str:
       return f"Staff(id={self.id!r}, first_name{self.first_name!r}, middle_name={self.middle_name!r}, last_name={self.last_name!r})"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class StaffSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "first_name", "middle_name", "last_name", "staff_code", "rank", "title", "user_id")


staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)