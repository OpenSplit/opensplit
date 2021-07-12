# Generated by Django 3.1.12 on 2021-06-07 20:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_auto_20210606_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='legacy_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together={('name', 'owner')},
        ),
    ]