# Generated by Django 3.2.15 on 2024-05-22 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visuwallsproducts', '0004_productinventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('product_inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_requests', to='visuwallsproducts.productinventory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Booking Request',
                'verbose_name_plural': 'Booking Requests',
            },
        ),
    ]
