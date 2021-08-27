# Generated by Django 3.0.8 on 2021-03-14 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jwt_auth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RefreshSession',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_key', models.CharField(default=jwt_auth.models.generate_random_string, max_length=40)),
                ('expire_date', models.DateTimeField(default=jwt_auth.models.get_refresh_expire_date)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refresh_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'refresh_sessions',
            },
        ),
    ]