from django.db import models

# Create your models here.
from django.conf import settings


class Reward(models.Model):
    product_name = models.CharField(max_length=100)

    product_type = models.CharField(max_length=100)

    company_name = models.CharField(max_length=100)

    product_img = models.CharField(max_length=200)

    start_time = models.CharField(max_length=100)

    end_time = models.CharField(max_length=100)

    total_amount = models.PositiveIntegerField()

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='like_user'
    )

    def __str__(self):
        return self.product_name
