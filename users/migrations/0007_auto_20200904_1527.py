# Generated by Django 3.0.8 on 2020-09-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200904_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alahaberrysetting',
            name='unit_sale_charges',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]