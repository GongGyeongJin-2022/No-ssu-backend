# Generated by Django 3.2.14 on 2022-08-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220818_0325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marker',
            old_name='sizes',
            new_name='size',
        ),
        migrations.AlterField(
            model_name='marker',
            name='explanation',
            field=models.TextField(default=''),
        ),
    ]