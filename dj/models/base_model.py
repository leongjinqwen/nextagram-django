import os
# import peewee as pw
from django.db import models
import datetime
from database import db


class MyModelBase(models.base.ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name != "BaseModel":
            class Meta:
                db_table = name.lower()

            attrs["Meta"] = Meta

        r = super().__new__(cls, name, bases, attrs, **kwargs)
        return r


class BaseModel(models.Model, metaclass=MyModelBase):
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
