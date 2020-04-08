import os
# import peewee as pw
from django.db import models
import datetime
from database import db

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            result = super(BaseModel, self).save(*args, **kwargs)
            return True
        else:
            return 0

    def validate(self):
        print(
            f"Warning validation method not implemented for {str(type(self))}")
        return True

    

    class Meta:
        abstract = True