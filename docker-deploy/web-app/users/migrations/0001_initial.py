# Generated by Django 4.0.1 on 2022-01-31 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=200)),
                ('vehicle_type_registered', models.CharField(default='', max_length=200)),
                ('license_plate_number', models.CharField(default='', max_length=200)),
                ('capacity_of_the_car', models.IntegerField()),
                ('spacial_request', models.CharField(default='', max_length=200)),
            ],
        ),
    ]