import peewee as pw
from werkzeug.security import generate_password_hash

from models.base_model import BaseModel


class User(BaseModel):
    username = pw.CharField(unique=False)
    password = pw.CharField()
    email = pw.CharField(unique=True)

    def validate(self):
        # Password length validation
        if len(self.password) < 8:
            self.errors.append(
                'Password length needs to be at least 8 characters long.')
        else:
            self.password = generate_password_hash(self.password)

        # Check if username is unique
        # Check if email is unique?
        #
