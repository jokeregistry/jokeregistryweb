from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):

    username = models.CharField(max_length=25)
    USERNAME_FIELD = 'username'
