# Generated by Django 3.2.15 on 2024-05-27 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visuwallsproducts', '0008_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmbooking',
            name='status',
            field=models.CharField(choices=[('BORROWED', 'Borrowed'), ('RETURNED', 'Returned')], default='BORROWED', max_length=10),
        ),
    ]