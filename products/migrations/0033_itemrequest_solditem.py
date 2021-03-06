# Generated by Django 3.0.8 on 2021-02-28 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0032_auto_20210214_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_items', models.PositiveIntegerField(default=1)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=15)),
                ('date_requested', models.DateTimeField(default=django.utils.timezone.now)),
                ('clerk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoldItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ItemRequest')),
            ],
        ),
    ]
