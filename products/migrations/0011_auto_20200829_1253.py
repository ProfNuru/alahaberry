# Generated by Django 3.0.8 on 2020-08-29 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200731_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='Damage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='product_damages')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_damages',
        ),
        migrations.AddField(
            model_name='product',
            name='product_image1',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image2',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image3',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='category_image1',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='category_pics'),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='category_image2',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='category_pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.TextField(blank=True, null=True, verbose_name='Hash tags'),
        ),
        migrations.DeleteModel(
            name='ProductPhoto',
        ),
        migrations.AddField(
            model_name='damage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
