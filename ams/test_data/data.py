from .. import db
from ..models.User import User
from ..models.Staff import Staff


def seed_data():
    
    user1 = User(username='francis', email='francis@bolton.ac.uk', telephone='78124523', password='password', is_staff=True)
    staff1 = Staff(first_name='Francis', last_name='Morris', staff_code='7813', users=user1)
    db.session.add_all([user1])
    db.session.add_all([staff1])
    db.session.commit()