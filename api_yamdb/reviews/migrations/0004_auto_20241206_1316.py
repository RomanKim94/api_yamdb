# Generated by Django 3.2 on 2024-12-06 08:16

import django.core.validators
from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20241206_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator(message='Некоректный код подтверждения.', regex='^[ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]{10}$')], verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex=r'^[\w.@+-]+\Z'), reviews.validators.validate_invalid_username], verbose_name='Логин'),
        ),
    ]
