from .. import db
from ..models.User import User
from ..models.Staff import Staff


def seed_data():
    
    user1 = User(username='francis', email='francis@bolton.ac.uk', telephone='78124523', password='password', is_staff=True)
    db.session.add(user1)
    db.session.commit()