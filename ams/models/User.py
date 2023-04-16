from sqlalchemy import Identity
from .. import db
from .. import ma

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=True)
    is_student = db.Column(db.Boolean, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True)
    staff = db.relationship('Staff', backref='users')
    student = db.relationship('Student', backref='users')
    attendances_updated_by = db.relationship('ModuleLessonAttendance', backref='users')
    
    def __repr__(self):
        return f"User(id={self.id!r}, username{self.username!r})"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "username", "email", "telephone", "is_active")


user_schema = UserSchema()
users_schema = UserSchema(many=True)