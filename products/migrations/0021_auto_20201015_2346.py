# Generated by Django 3.0.8 on 2020-10-15 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_auto_20200929_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='area',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True, null=True, verbose_name='Where do you want the item delivered?'),
        ),
        migrations.AlterField(
            model_name='order',
            name='house_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='recipient',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Recipient name (Leave empty if you are the recipient)'),
        ),
    ]