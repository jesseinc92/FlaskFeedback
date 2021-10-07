from flask import Flask, render_template, redirect, session
from flask_wtf import form
from models import Feedback, db, connect_db, User, Feedback
from forms import CreateUserForm, LoginUserForm, CreateFeedbackForm


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
        
        session['user'] = new_user.username
        
        return redirect(f'/users/{username}')
    
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
            session['user'] = user.username
            return redirect(f'/users/{username}')
        
        else:
            form.username.errors = ['Incorrect username or password.']
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    '''Logs out a user and clears the session.'''
    
    session.pop('user')
    
    return redirect('/')


@app.route('/users/<username>')
def secret_page(username):
    '''Only registered users can access this page.'''
    
    if 'user' not in session:
        return redirect('/')
    
    else:
        user = User.query.filter_by(username=username).first()
        return render_template('info.html', user=user)
    
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''Deletes user from the database.'''
    
    if username == session['user']:
    
        # delete all user feedback from database
        posts = Feedback.query.filter_by(username=username).all()
        for post in posts:
            db.session.delete(post)
            db.session.commit()
                    
        # delete user from database
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        
        # clear all user information from session
        session.pop('user')
        
        return redirect('/')
    
    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_user_feedback(username):
    '''Adds feedback that is associated with the logged in user.'''
    
    if 'user' not in session:
        return redirect('/login')
    
    else:
        form = CreateFeedbackForm()
        if form.validate_on_submit():
            
            title = form.title.data
            content = form.content.data
            
            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            
            return redirect(f'/users/{username}')
        
        return render_template('feedback.html', form=form)
    
    
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    '''Displays a form to update user-specific feedback.'''
    
    post = Feedback.query.get(feedback_id)
    
    if 'user' not in session:
        return redirect('/login')
    
    if session['user'] == post.user.username:
        
        form = CreateFeedbackForm(obj=post)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            post.title = title
            post.content = content
            db.session.commit()
            
            return redirect(f'/users/{post.user.username}')
            
        return render_template('update-feedback.html', form=form)
    
    else:
        return redirect(f'/users/{post.user.username}')
    


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''Deletes a comment from the database.'''
    
    post = Feedback.query.get(feedback_id)
    
    if 'user' not in session:
        return redirect('/login')
    
    if session['user'] == post.user.username:
        db.session.delete(post)
        db.session.commit()
    
        return redirect(f'/users/{post.user.username}')
    
    else:
        return redirect('/login')