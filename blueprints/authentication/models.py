from app import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from sqlalchemy.dialects.postgresql import UUID
from flask_admin import Admin
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    is_customer = db.Column(db.Boolean, default=False)
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        self.password = generate_password_hash(original_password)

    def check_hashed_password(self, original_password):
        return check_password_hash(self.password, original_password)

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'username', 'email']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'is_customer': self.is_customer
        }
        return data

@login.user_loader
def load_user(id):
    return User.query.get(int(id))