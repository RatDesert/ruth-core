# Generated by Django 3.0.8 on 2021-08-16 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='refreshsession',
            name='http_user_agent',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='refreshsession',
            name='remote_addr',
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AddField(
            model_name='refreshsession',
            name='remote_host',
            field=models.TextField(null=True),
        ),
    ]