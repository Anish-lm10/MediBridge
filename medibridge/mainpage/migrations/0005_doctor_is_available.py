# Generated by Django 5.1.3 on 2024-12-04 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_doctor_user_doctor_verified_patient_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]
