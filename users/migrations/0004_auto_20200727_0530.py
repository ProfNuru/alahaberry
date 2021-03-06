# Generated by Django 3.0.8 on 2020-07-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_business_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alahaberrysetting',
            name='setting_key',
        ),
        migrations.RemoveField(
            model_name='alahaberrysetting',
            name='setting_value',
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='application_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='contact1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='contact2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='contact3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='facebook_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='google_map',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='google_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='instagram_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='linkedin_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='logo',
            field=models.ImageField(default='default.jpg', upload_to='application_images'),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='region',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='twitter_url',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
