# Generated by Django 3.1.2 on 2021-03-01 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discordlogin', '0004_auto_20210117_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geodata',
            name='city',
        ),
        migrations.RemoveField(
            model_name='geodata',
            name='country_code',
        ),
        migrations.RemoveField(
            model_name='geodata',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='geodata',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='geodata',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='geodata',
            name='region_name',
        ),
    ]
