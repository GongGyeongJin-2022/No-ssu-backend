# Generated by Django 3.2.14 on 2022-07-18 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220717_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, validators=[django.core.validators.RegexValidator('^010-?[1-9]\\d{4}-?\\d{4}$')]),
        ),
    ]