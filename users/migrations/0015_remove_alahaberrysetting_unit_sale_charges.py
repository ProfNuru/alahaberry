# Generated by Django 3.0.8 on 2020-09-28 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20200928_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alahaberrysetting',
            name='unit_sale_charges',
        ),
    ]
