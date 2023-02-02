import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_web_app.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_message = "Please log in to access this page."
login_manager.login_view = "login"


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (self.username, self.email)


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz', methods=['GET'])
def quiz():
    # Define the API endpoint
    endpoint = "https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple"

    # Make a request to the API
    response = requests.get(endpoint)
    data = response.json()

    # Extract the questions from the API response
    questions = data['results']

    return render_template('quiz.html', questions=questions)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    user = User.query.filter_by(name=name).first()
    if not user:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

    answers = []
    for key in request.form:
        if key != "name":
            answers.append(Answer(question=key, answer=request.form[key], user_id=user.id))

    score = 0
    for question, correct_answer in questions:
        user_answer = [a.answer for a in answers if a.question == question]
        if user_answer and user_answer[0] == correct_answer:
            score += 1

    db.session.add(Score(score=score, user_id=user.id))
    db.session.commit()

    return "Score: {}".format(score)


@app.route('/ranking')
def ranking():
    return render_template('ranking.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash(f"You are logged in as {user.email}", "success")
            return redirect(url_for('index'))
        else:
            flash("Wrong email or password", "danger")
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            # Return an error message if the passwords do not match
            return 'Passwords do not match'

        # Use SQLAlchemy to add the new user to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
