# Generated by Django 3.0.8 on 2020-07-21 00:58

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
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False)),
                ('subscription_type', models.TextField()),
                ('years', models.IntegerField(default=0)),
                ('months', models.IntegerField(default=0)),
                ('date_subscribed', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscription_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('business_name', models.CharField(default='NA', max_length=100)),
                ('business_address', models.TextField(default='NA', max_length=200)),
                ('business_city', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(default='NA', max_length=100)),
                ('date_registered', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscription_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
