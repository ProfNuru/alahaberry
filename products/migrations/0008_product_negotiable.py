# Generated by Django 3.0.8 on 2020-07-27 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200725_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='negotiable',
            field=models.BooleanField(default=False),
        ),
    ]