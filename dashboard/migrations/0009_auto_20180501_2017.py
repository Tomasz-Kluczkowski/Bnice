# Generated by Django 2.0.3 on 2018-05-01 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20180501_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='oopsy',
            name='points_remaining',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='smiley',
            name='points_remaining',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
