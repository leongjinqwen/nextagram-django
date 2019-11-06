from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=False)
    password = pw.CharField()
    email = pw.CharField(unique=True)

    def validate(self):
        return len(self.password) >= 6
