# Generated by Django 5.0.6 on 2024-06-09 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visuwallsproducts", "0017_alter_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingrequest",
            name="project_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
