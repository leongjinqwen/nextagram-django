from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=False)
    password = pw.CharField()
    email = pw.CharField(unique=True)

    def validate(self):
        # Password length validation
        if len(self.password) < 8:
            self.errors.append(
                'Password length needs to be at least 8 characters long.')

        # Check if username is unique
