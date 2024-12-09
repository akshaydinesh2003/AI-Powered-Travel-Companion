from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ai import generate_trip_plan 



##from flask import Flask, render_template, request ,redirect ,url_for, flash
##from flask_sqlalchemy import SQLAlchemy
##from flask_login import UserMixin, LoginManager , login_user, login_required, logout_user, current_user
##from werkzeug.security import generate_password_hash, check_password_hash



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


@app.route('/plan', methods=['POST'])
def plan_trip():
    # Get inputs from the form
    destination = request.form['destination']
    budget = request.form['budget']
    days = request.form['days']
    
    # Call the function in ai.py
    trip_plan = generate_trip_plan(destination, budget, days)
    
    # Render the output
    return render_template('plan.html', trip_plan=trip_plan, destination=destination)


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



#printing the trip plan

@app.route('/tripplan')
def tripplan():
    return render_template('tripplan.html')




app.run(debug=True)




    
