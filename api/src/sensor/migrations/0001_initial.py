# Generated by Django 3.0.8 on 2020-08-17 14:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('max_val', models.IntegerField()),
                ('min_val', models.IntegerField()),
                ('type', models.CharField(max_length=128)),
                ('dimension', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'sensor_models',
            },
        ),
        migrations.CreateModel(
            name='SensorLicense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.UUIDField(default=uuid.uuid4)),
                ('is_used', models.BooleanField(default=False)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sensor.SensorModel')),
            ],
            options={
                'db_table': 'sensor_licenses',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='hub.Hub')),
                ('license', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sensor.SensorLicense')),
            ],
            options={
                'db_table': 'sensors',
            },
        ),
    ]
