import os
import tempfile

import pytest
from ams import create_app, db
from ams.test_data import data


@pytest.fixture()
def app():
    
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config.update({
        "TESTING": True,
        'DATABASE': db_path,
    })

    # other setup can go here
    with app.app_context():
        #db.drop_all() 
        db.create_all()
        #data.seed_data() 

    yield app

    # clean up / reset resources here
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='francis', password='password'):
        return self._client.post(
            '/api/v1/auth/login',
            json={
                "username": username, "password": password
            }
        )

    # def logout(self):
    #     return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)