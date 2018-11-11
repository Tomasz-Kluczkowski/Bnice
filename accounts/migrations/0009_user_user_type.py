# Generated by Django 2.0.3 on 2018-10-13 10:32
from accounts.models import User

from django.db import migrations, models


def move_to_user_type(apps, schema_editor):
    existing_users = apps.get_model('accounts', 'User').objects.all()
    for user in existing_users:
        if user.is_superuser:
            user.user_type = User.TYPE_ADMIN
            user.save()
        elif user.is_parent:
            user.user_type = User.TYPE_PARENT
            user.save()
        elif user.is_child:
            user.user_type = User.TYPE_CHILD
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20180430_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(editable=False, max_length=30, null=True),
        ),
        migrations.RunPython(move_to_user_type),
        migrations.RemoveField(
            model_name='user',
            name='is_parent',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_child',
        ),
    ]
