from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, \
    logout_user

from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://zekbeksehdyqxb:2bdd9ad5f34d7b2e01c23711228a5cf1fc1cbec5c7c91f4e535c8d69d0ed63e4@ec2-52-203-27-62.compute-1.amazonaws.com:5432/daev1o7tcfeo9o'

db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route("/", methods = ['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods =['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
# @login_required
def chat():

    if not current_user.is_authenticated:
        return "Please login before accessing chat"

    return "Chat with me"


@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    return "Logged out using flask-login"

if __name__ == '__main__':

    app.run(debug=True)
