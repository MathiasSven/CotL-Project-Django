# Generated by Django 3.1.2 on 2021-03-12 22:13

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cotlsite', '0013_auto_20210227_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='colour',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True),
        ),
    ]
