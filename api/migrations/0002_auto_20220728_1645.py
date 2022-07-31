# Generated by Django 3.2.14 on 2022-07-28 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='marker',
            name='cleanup_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cleanup_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='marker',
            name='tags',
            field=models.ManyToManyField(to='api.Tag'),
        ),
        migrations.AlterField(
            model_name='reward',
            name='gave_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='gave_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reward',
            name='received_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='marker',
            name='sizes',
            field=models.ManyToManyField(to='api.Size'),
        ),
    ]
