from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired


class CreateUserForm(FlaskForm):
    '''A form model to create/sign-up a new user.'''
    
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    
    
class LoginUserForm(FlaskForm):
    '''A form model to login existing user.'''
    
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
    
class CreateFeedbackForm(FlaskForm):
    '''A form that creates a new piece of feedback.'''
    
    title = StringField('Title')
    content = TextAreaField('Content')