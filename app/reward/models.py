from django.db import models

# Create your models here.
from django.conf import settings


class Product(models.Model):
    product_name = models.CharField(max_length=300)

    product_price = models.PositiveIntegerField(default=0)

    product_shipping_charge = models.PositiveIntegerField(default=0)

    product_expecting_departure_date = models.CharField(max_length=100)

    product_total_count = models.PositiveIntegerField(default=0)

    product_sold_count = models.PositiveIntegerField(default=0)

    product_on_sale = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product_name}'


class Reward(models.Model):
    product_name = models.CharField(max_length=100)

    product_type = models.CharField(max_length=100)

    company_name = models.CharField(max_length=100)

    product_img = models.CharField(max_length=200)

    interested_count = models.PositiveIntegerField(blank=True, default=0)

    start_time = models.CharField(max_length=100)

    end_time = models.CharField(max_length=100)

    cur_amount = models.PositiveIntegerField(blank=True, default=0)

    total_amount = models.PositiveIntegerField(default=0)

    product = models.ForeignKey(
        Product,
        blank=True,
        on_delete=models.CASCADE,
        related_name='rewards'
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='like_posts'
    )

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-pk']


class Comment(models.Model):
    reward = models.ForeignKey(
        Reward,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='comments'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment (post: {self.reward.pk}, user: {self.user.username})'

    @property
    def author(self):
        if self.is_deleted:
            return None
        return self.user

    @property
    def content(self):
        if self.is_deleted:
            return '삭제된 덧글 입니다.'
        return self.content

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
