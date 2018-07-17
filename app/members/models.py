from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
# Create your models here.


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):

    img_profile = models.ImageField(upload_to='user', blank=True)

    def __str__(self):
        return self.username
