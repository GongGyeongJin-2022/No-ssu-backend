# Generated by Django 3.2.14 on 2022-09-18 05:14

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_merge_20220918_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='image',
            field=models.FileField(blank=True, max_length=300, null=True, upload_to=api.models.date_upload_to),
        ),
    ]
