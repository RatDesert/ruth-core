# Generated by Django 3.0.8 on 2021-05-02 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0004_auto_20210502_2022'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='hub',
            name='hub_hub_unique_name_per_user',
        ),
        migrations.AddConstraint(
            model_name='hub',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='hub_unique_name_per_user'),
        ),
    ]