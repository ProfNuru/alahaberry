# Generated by Django 3.0.8 on 2020-09-08 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20200908_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.FileField(default='default.png', upload_to='ad_media'),
            preserve_default=False,
        ),
    ]
