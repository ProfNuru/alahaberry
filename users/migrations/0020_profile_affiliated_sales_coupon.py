# Generated by Django 3.0.8 on 2020-10-21 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliations', '0003_auto_20200927_1940'),
        ('users', '0019_auto_20201021_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='affiliated_sales_coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='affiliations.Coupon'),
        ),
    ]