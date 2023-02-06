import unittest
import requests_mock

from flask_login import current_user
from werkzeug.security import generate_password_hash

from quiz import app, db, User


class LoginTests(unittest.TestCase):
    def setUp(self):
        # Create a test client with test user
        self.client = app.test_client()
        self.client.testing = True
        app.app_context().push()
        db.drop_all()
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
        with app.test_request_context():
            # Send a POST request to the login endpoint with incorrect credentials
            response = self.client.post('/login', data=dict(username='testuser', email='testuser@example.com',
                                                            password='wrongpassword'), follow_redirects=True)
            # Assert that the user was not logged in
            self.assertTrue(current_user.is_anonymous)
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
        app.app_context().push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        # drop all tables
        db.drop_all()

    def test_register_successful(self):
        with app.test_request_context():
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
        with app.test_request_context():
            # Send a POST request to the register endpoint with password and confirm password fields not matching
            response = self.client.post('/register', data=dict(
                username='testuser',
                email='testuser@example.com',
                password='password',
                confirm_password='different_password'
            ), follow_redirects=True)
            # Assert that the user was not registered
            self.assertTrue(current_user.is_anonymous)

            # Assert that the user received an error message indicating password mismatch
            self.assertIn(b'Passwords do not match', response.data)


class QuizTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = app.test_client()

        # Use requests_mock to mock the API request
        self.mock = requests_mock.Mocker()
        self.mock.start()

    def tearDown(self):
        self.mock.stop()

    def test_quiz_GET(self):
        with app.test_request_context():
            self.mock = requests_mock.Mocker()
            self.mock.start()
            self.mock.register_uri(
                'GET',
                'https://opentdb.com/api.php?amount=10&difficulty=medium&type=multiple',
                text='{"results": [{"question": "Question 1", "correct_answer": "Answer 1"}]},',headers={'Content-Type': 'application/json'}

            )

            try:
                response = self.client.get('/quiz', follow_redirects=True)

                # Check that the response is 200 OK
                self.assertEqual(response.status_code, 200)

                # Check that the questions are displayed
                self.assertIn(b'question', response.data)
            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"Response data: {response.get_data(as_text=True)}")

    def test_quiz_POST(self):
        with app.test_request_context():

            # Define a mock response for the API request
            data = {
                'response_code':0,
                'results': [
                    {
                        'question': 'What is the capital of France?',
                        'correct_answer': 'Paris',
                    },
                    {
                        'question': 'What is the capital of Germany?',
                        'correct_answer': 'Berlin',
                    },
                ]
            }
            self.mock.post('https://opentdb.com/api.php?amount=10&difficulty=medium&type=multiple', json=data)

            # Send a POST request to the quiz endpoint with the form data
            response = self.client.post('/quiz', data={'difficulty': 'medium'}, follow_redirects=True)

            # Check that the response is 200 OK
            self.assertEqual(response.status_code, 200)

            # Check that the questions are displayed
            self.assertIn(b'question', response.data)


if __name__ == '__main__':
    unittest.main()
