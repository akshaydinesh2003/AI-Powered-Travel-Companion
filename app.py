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



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('home'))
        flash("Invalid username or password")
        return redirect(url_for('login'))
    return render_template("login.html")


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

@app.route('/services')
def services():
    app.logger.info("Accessing the services page")
    return render_template('services.html')


# route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))



app.run(debug=True)