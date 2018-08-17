import os

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models
# Create your models here.
from config.settings.base import STATIC_DIR


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):
    blank_image_path = os.path.join(STATIC_DIR, 'static')
    print(blank_image_path)
    img_profile = models.ImageField(
        upload_to='user',
        default=blank_image_path
    )

    nickname = models.CharField(max_length=16)

    # def __str__(self):
    #     return self.username

