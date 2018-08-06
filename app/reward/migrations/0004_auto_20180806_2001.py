# Generated by Django 2.0.7 on 2018-08-06 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reward', '0003_product_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_shipping_charge',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sold_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_total_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reward',
            name='cur_amount',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='reward',
            name='interested_count',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='reward',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rewards', to='reward.Product'),
        ),
        migrations.AlterField(
            model_name='reward',
            name='total_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
