# Generated by Django 3.0.8 on 2020-09-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20200928_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered_by',
            field=models.TextField(blank=True, null=True),
        ),
    ]
