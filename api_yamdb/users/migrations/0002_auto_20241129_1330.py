# Generated by Django 3.2 on 2024-11-29 08:30

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=10, validators=[core.validators.ConfirmationCodeValidator], verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=128, verbose_name='Пароль'),
        ),
    ]