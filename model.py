from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.username

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    time_Stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.post_id} - {self.title}"


with app.app_context():
    db.create_all()
