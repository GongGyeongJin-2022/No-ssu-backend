# Generated by Django 4.0.6 on 2022-07-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=20)),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('explanation', models.TextField()),
            ],
        ),
    ]