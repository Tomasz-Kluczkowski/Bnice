# Generated by Django 2.1.2 on 2018-11-11 22:30

from django.db import migrations, models


def add_email(apps, schema_editor):
    users_no_email = apps.get_model('accounts', 'User').objects.filter(email='')
    for user in users_no_email:
        user.email = 'please_add@email.com'
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20181111_1728'),
    ]

    operations = [
        migrations.RunPython(add_email),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
