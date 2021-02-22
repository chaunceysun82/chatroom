from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256

from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://zekbeksehdyqxb:2bdd9ad5f34d7b2e01c23711228a5cf1fc1cbec5c7c91f4e535c8d69d0ed63e4@ec2-52-203-27-62.compute-1.amazonaws.com:5432/daev1o7tcfeo9o'

db = SQLAlchemy(app)

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
        return "Logged in, finally!"

    return render_template("login.html", form=login_form)


if __name__ == '__main__':

    app.run(debug=True)
