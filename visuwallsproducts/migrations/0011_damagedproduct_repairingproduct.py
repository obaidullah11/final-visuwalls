# Generated by Django 3.2.15 on 2024-05-27 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visuwallsproducts', '0010_alter_confirmbooking_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='IN_PROGRESS', max_length=20)),
                ('confirm_booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visuwallsproducts.confirmbooking')),
            ],
        ),
        migrations.CreateModel(
            name='DamagedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('confirm_booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visuwallsproducts.confirmbooking')),
            ],
        ),
    ]
