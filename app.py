from flask import Flask, render_template, redirect, session
from flask_wtf import form
from wtforms.fields.simple import PasswordField
from models import db, connect_db, User
from forms import CreateUserForm, LoginUserForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'heathers21'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
db.create_all()


@app.route('/')
def root_directory():
    '''Redirects to the registration page.'''
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    '''Displays a registration form to create a new user.'''
    
    form = CreateUserForm()
    if form.validate_on_submit():
        
        # collect data and create user in external method
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        
        return redirect('/secret')
    
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    '''Displays a login form for returning users.'''
    
    # add form and show in template
    form = LoginUserForm()
    if form.validate_on_submit():
        
        # collect data and create user in external method
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        if user:
            session['user_id'] = user.id
            return redirect('/secret')
        
        else:
            form.username.errors = ['Incorrect username or password.']
    
    return render_template('login.html', form=form)


@app.route('/secret')
def secret_page():
    '''Only registered users can access this page.'''
    return 'You made it!'