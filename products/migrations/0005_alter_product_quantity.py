# Generated by Django 3.2.15 on 2024-05-20 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productinventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.CharField(blank=True, default=2, max_length=255),
            preserve_default=False,
        ),
    ]
