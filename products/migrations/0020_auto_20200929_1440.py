# Generated by Django 3.0.8 on 2020-09-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_order_delivered_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='area',
            field=models.CharField(max_length=100, null=True, verbose_name='Area'),
        ),
        migrations.AddField(
            model_name='order',
            name='closest_landmark',
            field=models.TextField(blank=True, null=True, verbose_name='Describe the closest landmark to your location'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(null=True, verbose_name='Where do you want the item delivered?'),
        ),
        migrations.AddField(
            model_name='order',
            name='house_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='recipient',
            field=models.CharField(max_length=100, null=True, verbose_name='Recipient name (Leave empty if you are the recipient)'),
        ),
    ]
