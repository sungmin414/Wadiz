# Generated by Django 2.0.7 on 2018-08-01 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_user_img_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]