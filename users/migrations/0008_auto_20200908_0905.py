# Generated by Django 3.0.8 on 2020-09-08 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200904_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alahaberrysetting',
            name='unit_sale_charges',
            field=models.FloatField(default=0.0, null=True, verbose_name='Percentage charge on sale'),
        ),
    ]