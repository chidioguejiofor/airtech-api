from airtech_api.utils.base_model import BaseModel
from django.db import models
from uuid import uuid4
from passlib.hash import pbkdf2_sha512


# Create your models here.
class User(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    gender = models.CharField(
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
        ),
        null=False,
        max_length=6)
    # gender = EnumChoiceField(enum_class=GenderEnum, null=False)
    date_of_birth = models.DateField(null=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    password_hash = models.TextField()
    email = models.EmailField(null=False, unique=True)
    _password = None

    class Meta:
        db_table = 'User'

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password_str):
        self._password = password_str
        self.password_hash = pbkdf2_sha512.hash(password_str)

    def verify_password(self, password_str):

        return pbkdf2_sha512.verify(password_str, self.password_hash)
