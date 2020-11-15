# Generated by Django 3.0.8 on 2020-10-24 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_profile_affiliated_sales_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='alahaberrysetting',
            name='commission_on_subscription',
            field=models.DecimalField(decimal_places=3, default=5.0, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='alahaberrysetting',
            name='commission_rate_on_sale',
            field=models.DecimalField(decimal_places=2, default=7.0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='alahaberrysetting',
            name='charges_on_sale',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5, null=True, verbose_name='Percentage charge on sale'),
        ),
    ]
