# Generated by Django 2.0.3 on 2018-10-14 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_oopsy_points_remaining'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oopsy',
            options={'ordering': ['earned_on']},
        ),
        migrations.AlterModelOptions(
            name='smiley',
            options={'ordering': ['earned_on']},
        ),
    ]
