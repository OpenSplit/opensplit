# Generated by Django 3.1.12 on 2021-06-07 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210607_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='legacy_id',
            field=models.IntegerField(null=True),
        ),
    ]
