# Generated by Django 3.2.15 on 2024-05-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visuwallsproducts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.CharField(max_length=255),
        ),
    ]
