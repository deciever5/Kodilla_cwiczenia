import unittest

from flask_login import current_user
from werkzeug.security import generate_password_hash

from quiz import app, db, User


class LoginTests(unittest.TestCase):
    def setUp(self):
        # Create a test client with test user
        self.client = app.test_client()
        self.client.testing = True
        with app.app_context():
            db.create_all()
        password = generate_password_hash('password', method='sha256')
        user = User(username='testuser', email='testuser@example.com', password=password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def test_login_successful(self):
        with app.test_request_context():
            response = self.client.post('/login', data={
                'email': 'testuser@example.com',
                'password': 'password'}, follow_redirects=True)
            # Assert that the user was logged in and redirected
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.email, 'testuser@example.com')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You are logged in as testuser', response.data)

    def test_login_unsuccessful(self):
        # Send a POST request to the login endpoint with incorrect credentials
        response = self.client.post('/login', data=dict(username='testuser', email='testuser@example.com',
                                                        password='wrongpassword'), follow_redirects=True)
        # Assert that the user was not logged in
        self.assertEqual(current_user, None)
        # Assert that the user was redirected to the login page and an error message was displayed
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wrong email or password', response.data)


class RegisterTestCase(unittest.TestCase):
    def setUp(self):
        # create a test client
        self.client = app.test_client()
        # propagate the exceptions to the test client
        self.client.testing = True
        # create the database and tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # drop all tables
        with app.app_context():
            db.drop_all()

    def test_register_successful(self):
        # Send a POST request to the register endpoint with sample user's credentials
        email = 'testuser@example.com'
        response = self.client.post('/register', data=dict(
            username='testuser',
            email=email,
            password='password',
            confirm_password='password'
        ), follow_redirects=True)

        # Assert that the user was registered successfully
        user = User.query.filter_by(email=email).first()
        self.assertEqual(user.username, 'testuser')
        # Assert that the user was redirected to the quiz page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are registered as testuser', response.data)

    def test_register_password_mismatch(self):
        # Send a POST request to the register endpoint with password and confirm password fields not matching
        response = self.client.post('/register', data=dict(
            username='testuser',
            email='testuser@example.com',
            password='password',
            confirm_password='different_password'
        ), follow_redirects=True)

        # Assert that the user was not registered
        self.assertEqual(current_user, None)

        # Assert that the user received an error message indicating password mismatch
        self.assertIn(b'Passwords do not match', response.data)

    if __name__ == '__main__':
        unittest.main()
