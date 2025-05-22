from app.extensions import db
from datetime import datetime

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='client')  # 'client' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())

    def __init__ (self, name, email, password, role='Client'):
         super(User, self).__init__()
         self.name = name
         self.email = email
         self.password = password
         self.role = role

    def user_info(self):
       return  f" {self.name}"