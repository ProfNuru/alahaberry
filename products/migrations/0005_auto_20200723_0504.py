# Generated by Django 3.0.8 on 2020-07-23 05:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
