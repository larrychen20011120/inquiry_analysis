from app import db, loginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    quota = db.Column(db.Integer, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @loginManager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'<User {self.name}>'

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    patient = db.Column(db.String(64), nullable=True)
    url = db.Column(db.String(128), unique=True, nullable=False)
    completed = db.Column(db.Boolean())
    userId = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<File {self.url}>'

class AnalysisResult(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    fileId = db.Column(db.Integer, unique=True)
    result_url = db.Column(db.String(128), unique=True, nullable=False)
    wordcloud_url = db.Column(db.String(128), unique=True, nullable=False)
    def __repr__(self):
        return f'<Result {self.result_url}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    fileId = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return f'<Result {self.fileId}>'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, nullable=False)
    fileId = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return f'<Result {self.owner}>'
