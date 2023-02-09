import unittest
import pytest
import requests_mock
from flask_login import current_user
from werkzeug.security import generate_password_hash
from quiz import app, db, User, Score
import sys
import platform

# solution for a bug which causes errors while trying to run pytest on Windows machine withc python version >= 3.9
if sys.version_info >= (3, 9) and platform.system() == "Windows":
    import collections
    collections.Callable = collections.abc.Callable



class LoginTests(unittest.TestCase):
    def setUp(self):
        # Create a test client with test user
        self.client = app.test_client()
        self.client.testing = True
        app.app_context().push()
        db.drop_all()
        db.create_all()
        password = generate_password_hash('password', method='sha256')
        user = User(username='testuser', email='testuser@example.com', password=password)  # type: ignore
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
            self.assertTrue(current_user.is_active)
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


class RankingTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = app.test_client()
        # Create a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.app_context().push()
        db.drop_all()
        db.create_all()
        self.mock = requests_mock.Mocker()
        self.mock.start()
        self.mock.register_uri(
            'GET',
            'https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple',
            json={"results": [
                {"question": "Question 1", "correct_answer": "Answer 1",
                 "incorrect_answers": ["Wrong anwser", "Another wrong anwser"]}]},
            headers={'Content-Type': 'application/json'}

        )
        # Create test data
        user = User(username='test_user')  # type: ignore
        db.session.add(user)
        db.session.commit()
        score = Score(user_id=user.id, score=100)
        db.session.add(score)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_ranking_GET(self):
        response = self.client.get('/ranking', follow_redirects=True)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the ranking is displayed
        self.assertIn(b"Rankings", response.data)

        # Check that the test data is displayed
        self.assertIn(b"100", response.data)


@pytest.fixture(scope="class")
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()
    yield client

@pytest.fixture(scope="class")
def user(client):
    db.create_all()
    password = generate_password_hash('testpassword', method='sha256')
    user = User(email='testuser@example.com', username='testuser', password=password)
    db.session.add(user)
    db.session.commit()
    with app.test_request_context():
        client.post('/login', data={'email': 'testuser@example.com', 'password': 'testpassword'}, follow_redirects=True)
    yield user

def test_logout(client, user):
    with app.test_request_context():
        assert current_user.is_authenticated
        response = client.get('/logout')

        assert response.status_code == 302
        assert response.location == '/'
        assert not current_user.is_authenticated

class SubmitTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        app.app_context().push()
        db.create_all()

        user = User(username='test_user')  # type: ignore
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_submit_POST(self):
        with app.test_request_context():
            with app.test_client() as client:
                # login the user
                user = User(username='test_user')  # type: ignore

                with client.session_transaction() as sess:
                    sess['questions'] = [{"question": "Question 1", "correct_answer": "Answer 1"}]

                # Make a POST request to the submit endpoint
                response = client.post('/submit', data={
                    "Question 1": "Answer 1"
                })

                # Check that the response is a redirect to the index endpoint
                self.assertEqual(response.status_code, 302)

                # Check that the score was added to the database
                score = Score.query.first()
                self.assertIsNotNone(score)
                self.assertEqual(score.score, 1)
                self.assertEqual(score.user_id, user.id)


class QuizTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = app.test_client()
        # Use requests_mock to mock the API request
        self.mock = requests_mock.Mocker()
        self.mock.start()
        app.app_context().push()
        db.drop_all()
        db.create_all()
        password = generate_password_hash('password', method='sha256')
        user = User(username='testuser', email='testuser@example.com', password=password)  # type: ignore
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        self.mock.stop()

    def test_quiz_GET(self):
        with app.test_client() as client:
            self.client.post('/login', data={
                'email': 'testuser@example.com',
                'password': 'password'}, follow_redirects=True)
            self.mock = requests_mock.Mocker()
            self.mock.start()
            self.mock.register_uri(
                'GET',
                'https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple',
                json={"results": [
                    {"question": "Question 1", "correct_answer": "Answer 1",
                     "incorrect_answers": ["Wrong anwser", "Another wrong anwser"]}]},
                headers={'Content-Type': 'application/json'}

            )
            response = client.get('/quiz', follow_redirects=True)
            # print(response)
            # Check that the response is 200 OK
            self.assertEqual(response.status_code, 200)

            # Check that the questions are displayed
            self.assertIn(b'quiz', response.data)

    def test_quiz_POST(self):
        with app.test_request_context():
            self.client.post('/login', data={
                'email': 'testuser@example.com',
                'password': 'password'}, follow_redirects=True)
            # Define a mock response for the API request
            data = {
                'response_code': 200,
                'results': [
                    {
                        'question': 'What is the capital of France?',
                        'correct_answer': 'Paris',
                        'incorrect_answers': ['Leszno', 'Wschowa', 'Szlichtyngowa'],
                    },
                    {
                        'question': 'What is the capital of Germany?',
                        'correct_answer': 'Berlin',
                        'incorrect_answers': ['Leszno', 'Wschowa', 'Szlichtyngowa'],
                    },
                ]
            }
            with requests_mock.Mocker() as m:
                m.get('https://opentdb.com/api.php?amount=10&difficulty=hard&type=multiple', json=data)

                # Send a POST request to the quiz endpoint with the form data
                response = self.client.post('/quiz', data={'difficulty': 'hard'}, follow_redirects=True)

            # Check that the response is 200 OK
            self.assertEqual(response.status_code, 200)

            # Check that the questions are displayed
            self.assertIn(b'France', response.data)


if __name__ == '__main__':
    unittest.main()
