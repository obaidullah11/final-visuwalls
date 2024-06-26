# Generated by Django 3.2.15 on 2024-05-20 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0006_bookingrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed_date', models.DateTimeField(auto_now_add=True)),
                ('booking_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='confirm_booking', to='products.bookingrequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirm_bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
