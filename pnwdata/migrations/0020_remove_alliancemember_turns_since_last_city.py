# Generated by Django 3.1.2 on 2021-07-04 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pnwdata', '0019_auto_20210704_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alliancemember',
            name='turns_since_last_city',
        ),
    ]
