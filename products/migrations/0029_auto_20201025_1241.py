# Generated by Django 3.0.8 on 2020-10-25 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_producthits_date_viewed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductHits',
            new_name='ProductHit',
        ),
    ]
