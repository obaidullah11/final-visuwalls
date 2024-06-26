# Generated by Django 5.0.6 on 2024-06-09 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visuwallsproducts", "0015_alter_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="productimages/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
