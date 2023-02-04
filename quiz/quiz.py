import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, logout_user, current_user, login_required, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy import Integer, Column, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_web_app.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Answer(db.Model):
    __tablename__ = 'user_answers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question = Column(String(200))
    answer = Column(String(100))

    def __repr__(self):
        return "<UserAnswer(user_id='%s', question='%s', answer='%s')>" % (self.user_id, self.question, self.answer)


class Score(db.Model):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    score = Column(Integer)

    def __repr__(self):
        return "<Score(user_id='%s', score='%s')>" % (self.user_id, self.score)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        print(generate_password_hash(password))
        print(user.password)
        if user and (check_password_hash(user.password, password)):
            login_user(user)  # log the user in
            flash(f"You are logged in as {user.username}", "success")
            return redirect(url_for('index'))
        else:
            flash("Wrong email or password", "danger")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            # Return an error message if the passwords do not match
            flash("Passwords do not match", "danger")
            return render_template('register.html')

        # Use SQLAlchemy to add the new user to the database

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(
                password,
                method='sha256'
            )
        )
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        login_user(user)
        if user is not None:
            flash(f"You are registered as {username}", "success")
        else:
            flash("Not registered. Please try again", "danger")

        return redirect(url_for('quiz'))

    return render_template('register.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    difficulty = 'easy'
    endpoint = "https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple"
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        endpoint = f'https://opentdb.com/api.php?amount=10&difficulty={difficulty}&type=multiple'
    # Make a request to the API
    response = requests.get(endpoint)
    data = response.json()
    # Extract the questions from the API response
    questions = data['results']
    session['questions'] = questions
    return render_template('quiz.html', questions=questions, difficulty=difficulty)


@app.route("/submit", methods=["POST"])
@login_required
def submit():
    # Get the answers from the form data
    user_quiz = request.form
    phrases = session['questions']
    score = 0
    for phrase in phrases:
        for (question, answer) in user_quiz.items():
            if phrase.get('question') == question and phrase.get('correct_answer') == answer:
                print('Got one!')
                score += 1

    user_id = session.get("user_id")
    print(user_id)
    # # Create a new Score object and add it to the database
    score = Score(score=score, user_id=user_id)
    db.session.add(score)
    db.session.commit()

    # Redirect the user to the quiz results page
    return redirect(url_for("index", score=score))


@app.route('/ranking')
def ranking():
    print(current_user)
    return render_template('ranking.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
