# Generated by Django 2.1.2 on 2018-10-23 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20181014_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oopsy',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oopsies', to='accounts.Child'),
        ),
        migrations.AlterField(
            model_name='smiley',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smileys', to='accounts.Child'),
        ),
    ]
