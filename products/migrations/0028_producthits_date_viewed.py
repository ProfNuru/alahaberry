# Generated by Django 3.0.8 on 2020-10-25 12:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_producthits'),
    ]

    operations = [
        migrations.AddField(
            model_name='producthits',
            name='date_viewed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
