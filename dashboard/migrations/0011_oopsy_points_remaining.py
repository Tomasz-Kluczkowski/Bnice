# Generated by Django 2.0.3 on 2018-05-01 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20180501_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='oopsy',
            name='points_remaining',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]