# Generated by Django 5.0.4 on 2024-07-31 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units_test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('single', 'One correct answer'), ('multiple', 'Several correct answers')], default='single', max_length=10),
        ),
    ]
