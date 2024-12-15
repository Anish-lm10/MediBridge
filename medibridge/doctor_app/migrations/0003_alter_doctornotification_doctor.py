# Generated by Django 5.1.3 on 2024-12-10 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0002_alter_doctornotification_doctor'),
        ('mainpage', '0005_doctor_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctornotification',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.doctor'),
        ),
    ]
