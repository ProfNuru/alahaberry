# Generated by Django 3.0.8 on 2020-09-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200903_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damage',
            name='image',
            field=models.ImageField(blank=True, upload_to='product_damages'),
        ),
    ]
