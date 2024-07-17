import unittest
from app import app, db
from models import UserTable, BlogPost

class BlogTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'your-own-test-db'
        self.app = app.test_client()
        db.create_all()
        user = UserTable(username='test')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()
        self.auth_headers = {'Authorization': 'Basic dGVzdDp0ZXN0'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_post(self):
        response = self.app.post('/api/posts', json={'title': 'Test', 'content': 'Test content'}, headers=self.auth_headers)
        self.assertEqual(response.status_code, 201)

    def test_get_posts(self):
        response = self.app.get('/api/posts')
        self.assertEqual(response.status_code, 200)

    def test_get_post(self):
        post = BlogPost(title='Test', content='Test content', user_id=1)
        db.session.add(post)
        db.session.commit()
        response = self.app.get(f'/api/posts/{post.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        post = BlogPost(title='Test', content='Test content', user_id=1)
        db.session.add(post)
        db.session.commit()
        response = self.app.put(f'/api/posts/{post.id}', json={'title': 'Updated'}, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        post = BlogPost(title='Test', content='Test content', user_id=1)
        db.session.add(post)
        db.session.commit()
        response = self.app.delete(f'/api/posts/{post.id}', headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
