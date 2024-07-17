import unittest
from app import app, db
from models import UserTable

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'Your own test DB' ## Follow instructions in config 
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        response = self.app.post('/auth/register', json={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        user = UserTable(username='test')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()
        response = self.app.post('/auth/login', headers={'Authorization': 'Basic dGVzdDp0ZXN0'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
