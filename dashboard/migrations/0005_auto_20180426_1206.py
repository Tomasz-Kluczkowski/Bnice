# Generated by Django 2.0.3 on 2018-04-26 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20180425_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='oopsy',
            name='points',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='smiley',
            name='points',
            field=models.IntegerField(default=3),
        ),
    ]
