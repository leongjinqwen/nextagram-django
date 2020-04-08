# import peewee as pw
from django.db import models
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from .base_model import BaseModel
import os
from django.core.exceptions import ObjectDoesNotExist
from playhouse.hybrid import hybrid_property


class User(UserMixin, BaseModel):
    username = models.CharField(max_length=100, unique=False)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=100, default="user")
    profile_picture = models.TextField(max_length=200, null=True)

    @classmethod
    def get_or_none(self, **kwargs):
        try:
            return User.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def validate(self):
        duplicate_username = User.get_or_none(username=self.username)
        duplicate_email = User.get_or_none(email=self.email)

        if duplicate_username and duplicate_username.id != self.id:
            self.errors.append('Username not unique')
        if duplicate_email and duplicate_email.id != self.id:
            self.errors.append('Email not unique')
        if len(self.password) < 8 or len(self.password) > 25:
            self.errors.append('Password must between 8-25 characters.')
        else:
            self.password = generate_password_hash(self.password)

    @hybrid_property
    def profile_image_url(self):
        return os.environ['S3_DOMAIN'] + self.profile_picture
