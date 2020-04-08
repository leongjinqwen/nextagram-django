# import peewee as pw
from django.db import models
from .base_model import BaseModel
from .user import User
import os

class Image(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.TextField(max_length=100)
