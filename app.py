from flask import Flask, render_template, url_for, redirect, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #for front end comms

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use a SQLite database
app.config['SECRET_KEY'] = 'thesecretkeytobechanged'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt=Bcrypt(app)

db = SQLAlchemy(app)

login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username=db.Column(db.String[20], nullable=False, unique = True)
    password=db.Column(db.String[80], nullable=False)
    accom=db.Column(db.String[80], nullable=False)
    course=db.Column(db.String[80], nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    accom = StringField(validators=[InputRequired()], render_kw={"placeholder":"Accomodation"})
    course = StringField(validators=[InputRequired()], render_kw={"placeholder":"Course"})

    submit = SubmitField("Register")

    def validate_username(self,username):
        existing_user_username=User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                "exists"
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")
        

def create_db():
    # Use the app context when creating the database
    with app.app_context():
        db.create_all()  # Creates tables based on the models

# @app.route('/img/<path:filename>')
# def custom_static(filename):
#     return send_from_directory('/img/', filename)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login', methods = {'GET', 'POST'})
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user : 
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('connections'))
    
    return render_template('login.html',form=form)

@app.route('/memePage')
@login_required
def memePage():
    return render_template('memePage.html')

@app.route('/connections')
@login_required
def connections():
    return render_template('connections.html')


@app.route('/logout', methods = {'GET', 'POST'})
@login_required
def logout():
    return redirect(url_for('login'))

@app.route('/register', methods = {'GET', 'POST'})
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, accom = form.accom.data, course = form.course.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('memePage'))
    
    return render_template('register.html',form=form)

# @app.route('/saveHumor', methods=['POST'])
# def save_humour():
#     # Get the array from the form data and parse it back from JSON
#     user_humour = request.form.get('humour')

#     # Send a response back to the client
#     return jsonify({"status": "success", "received_array": my_array})


if __name__ == "__main__":
    create_db()
    app.run(debug=True)