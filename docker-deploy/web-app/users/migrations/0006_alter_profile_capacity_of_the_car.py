# Generated by Django 4.0.1 on 2022-01-31 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_capacity_of_the_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='capacity_of_the_car',
            field=models.IntegerField(),
        ),
    ]
