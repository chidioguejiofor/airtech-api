from airtech_api.utils.base_model import BaseModel
from django.db import models
from passlib.hash import pbkdf2_sha512


# Create your models here.
class User(BaseModel):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    gender = models.CharField(choices=(
        ('Male', 'Male'),
        ('Female', 'Female'),
    ),
                              null=False,
                              max_length=6)
    date_of_birth = models.DateField(null=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    password_hash = models.TextField()
    email = models.EmailField(null=False, unique=True)
    admin = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    image_url = models.URLField(null=True)
    image_public_id = models.CharField(max_length=50, null=True)
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
