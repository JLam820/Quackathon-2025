from flask import Flask, render_template, url_for, redirect, jsonify, send_from_directory, request
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
    humor=db.Column(db.String[80], default="xxx") #allow to be empty!


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    accom = StringField(validators=[InputRequired()], render_kw={"placeholder":"Accomodation"})
    course = StringField(validators=[InputRequired()], render_kw={"placeholder":"Course"})
    # socials = StringField(validators=[InputRequired()], render_kw={"placeholder":"Social Media"})
    # gender = StringField(validators=[InputRequired()], render_kw={"placeholder":"Gender"})
    # age = StringField(validators=[InputRequired()], render_kw={"placeholder":"Age"})

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

# First Page
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
# @login_required
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
        new_user = User(username=form.username.data, password=hashed_password, 
                    accom = form.accom.data, course = form.course.data) #should auto add the humor 
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('memePage')) ### wtf
    
    # go to register the first time 
    return render_template('register.html',form=form)

# Saving the humor hehe 
@app.route('/saveHumor', methods=['POST'])
@login_required
def save_humor():
    data = request.json  # Get JSON data from the request

    # Check if the 'humor' key is in the JSON data
    if not data or "humor" not in data:
        return jsonify({"error": "Invalid data, humor field is required"}), 400
    
    # Find the current user from the session
    current_user.humor = data["humor"]  # Update the humor value for the logged-in user
    
    # Commit the changes to the database
    db.session.commit()

    # Return a success response with the updated humor value
    return jsonify({"message": "Humor value updated successfully!", "humor": current_user.humor}), 200

####################?????????????
@app.route('/matchHumor', methods=['GET'])
@login_required
def match_humor():
    # Get the current user's humor value
    # current_user_humor = current_user.humor
    current_user_humor = "xxx"

    # Query the database for users with the same humor value (excluding the current user)
    matching_users = User.query.filter_by(humor=current_user_humor).all()

    # Optionally, filter out the current user from the results
    matching_users = [user for user in matching_users if user.id != current_user.id]

    # return render_template('connections.html', users=matching_users)

     # Prepare the data to return as JSON
    users_data = [{"id": user.id, "username": user.username, "humor": user.humor} for user in matching_users]

    return jsonify(users_data)

if __name__ == "__main__":
    create_db()
    app.run(debug=True)