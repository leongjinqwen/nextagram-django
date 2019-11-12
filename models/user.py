import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from models.base_model import BaseModel
from config import Config

class User(UserMixin, BaseModel):
    username = pw.CharField(unique=False)
    password = pw.CharField()
    email = pw.CharField(unique=True)
    role = pw.CharField(default="user")
    profile_picture = pw.TextField(null=True)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username and duplicate_username.id != self.id:
            self.errors.append('Username not unique')
        if duplicate_email and duplicate_email.id != self.id :
            self.errors.append('Email not unique')
        if len(self.password) < 8 or len(self.password) > 25:
            self.errors.append('Password must between 8-25 characters.')
        else:
            self.password=generate_password_hash(self.password)

    def profile_image_url(self):
        return Config.S3_LOCATION + self.profile_picture
    