# Generated by Django 5.0.6 on 2024-06-10 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visuwallsproducts", "0019_alter_product_dynamic_attributes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="confirmbooking",
            name="status",
            field=models.CharField(
                choices=[
                    ("BOOKING", "didnt recieved"),
                    ("BORROWED", "Borrowed  "),
                    ("RETURNED", "Returned"),
                ],
                default="BOOKING",
                max_length=10,
            ),
        ),
    ]
