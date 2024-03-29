from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)
    
    
class User(db.Model):
    '''A database model for users.'''
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    
    @classmethod
    def register(cls, username, password, email, first, last):
        '''Registers a user.'''
        
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)
        
        
    @classmethod
    def authenticate(cls, username, password):
        '''Authenticates a user.'''
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        
        else:
            return False
        
        
        
class Feedback(db.Model):
    '''A model for creating user-specific feedback content.'''
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    
    user = db.relationship('User', backref='comments')