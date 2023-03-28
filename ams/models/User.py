from sqlalchemy import Identity
from .. import db
from .. import ma

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, Identity(start=10, cycle=True), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=True)
    is_student = db.Column(db.Boolean, nullable=True)
    staff = db.relationship('Staff', backref='users')
    student = db.relationship('Student', backref='users')
    
    def __repr__(self):
        return f"User(id={self.id!r}, username{self.username!r})"
        return "<User(username={self.username!r})>".format(self=self)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
<<<<<<< HEAD
        fields = ("id", "username", "email", "telephone", "_links")

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )
=======
        fields = ("id", "username", "email", "telephone")
>>>>>>> 9dac22e760932c03ceb9675d5e49d18e3c05fd35


user_schema = UserSchema()
users_schema = UserSchema(many=True)