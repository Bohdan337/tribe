# Generated by Django 5.0.4 on 2024-06-24 16:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_alter_schedule_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='datetime',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
