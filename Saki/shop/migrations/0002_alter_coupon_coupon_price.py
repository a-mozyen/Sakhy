# Generated by Django 4.2.7 on 2023-12-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_price',
            field=models.FloatField(),
        ),
    ]
