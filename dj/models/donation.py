# import peewee as pw
from django.db import models
from .base_model import BaseModel
from .user import User
from .image import Image

class Donation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
