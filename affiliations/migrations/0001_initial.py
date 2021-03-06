# Generated by Django 3.0.8 on 2020-09-26 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(default='NA', max_length=100)),
                ('sponsorship', models.BooleanField(default=False)),
                ('discount_rate', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiry_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('date_used', models.DateTimeField(default=django.utils.timezone.now)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiliations.Coupon')),
            ],
        ),
    ]
