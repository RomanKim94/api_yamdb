# Generated by Django 3.2 on 2024-12-05 08:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='Некоректный код подтверждения.', regex='^[A-Z\\d]{10}$')], verbose_name='Код подтверждения'),
        ),
    ]
