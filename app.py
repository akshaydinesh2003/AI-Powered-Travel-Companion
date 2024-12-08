from flask import Flask, render_template, request ,redirect ,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager , login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

app.secret_key = 'MITS@123'


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('trips', lazy=True))




app.app_context().push()
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user:
            flash ("User already exists")
            return redirect(url_for('signup'))
        hashed_password=generate_password_hash(password,method='pbkdf2:sha256')
        user=User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
        flash("Invalid username or password")
        return redirect(url_for('login'))
    return render_template("login.html")



@app.route('/createtrip', methods=['GET', 'POST'])
@login_required
def createtrip():
    if request.method == 'POST':
        destination = request.form['destination']
        days = request.form['days']
        budget = request.form['budget']
        
        # Save the trip to the database
        new_trip = Trip(destination=destination, days=days, budget=budget, user_id=current_user.id)
        db.session.add(new_trip)
        db.session.commit()
        
        # Redirect to the dashboard
        flash("Trip created successfully!")
        return redirect(url_for('dashboard'))
    return render_template('createtrip.html')




@app.route('/')
def hello_world():
    return render_template('basic.html')


@app.route('/landing')
def landing():
    return render_template('landing.html')



@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')  
def contact():
    return render_template('contact.html')

'''@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', name=current_user.username)'''
@app.route('/dashboard')
@login_required
def dashboard():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', name=current_user.username, trips=trips)


@app.route('/services')
def services():
    return render_template('services.html')



# route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))



app.run(debug=True)




"""#The "AI-Powered Travel Companion" is a web-based platform that helps users plan trips tailored to their desired destination and budget. By simplifying travel planning, the system provides users with personalized itineraries and budget-friendly recommendations, ensuring a seamless and enjoyable travel experience. Users begin by entering their travel destination and budget into the platform. Based on this information, the system generates a virtual trip plan, including accommodation, transportation, activities, and dining options, all within the specified budget. A user profile and financial dashboard allow travelers to view and adjust their trip preferences, with the budget management system dynamically allocating funds across various trip components. An AI-powered interactive chatbot enhances the platform, offering travel advice, answering destination-related queries, and providing insights into the itinerary. The platform integrates real-time data from travel and accommodation APIs to ensure up-to-date and accurate planning options. This project combines generative AI and web development to create a practical solution for personalized travel planning. It eliminates the complexity of organizing trips, enabling users to make the most of their travel experiences while adhering to their financial constraints.
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret='MITS@123'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

app.app_context().push()
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user:
            flash ("User already exists")
            return redirect(url_for('signup'))
        hashed_password=generate_password_hash(password,method='pbkdf2:sha256')
        user=User(username=username,email=email,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid password')
                return redirect(url_for('login'))
        else:
            flash('User does not exist')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def hello_world():
    return render_template('basic.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
"""
    