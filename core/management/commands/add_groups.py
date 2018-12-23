from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from core.permissions import GroupPermissionSetter


class Command(BaseCommand):
    """
    Use to add all necessary groups.
    """
    help = 'Add groups in the database.'

    def handle(self, *args, **kwargs):
        print('Adding groups.')
        counter = 0
        for group in GroupPermissionSetter.GROUPS:
            group, created = Group.objects.get_or_create(name=group)
            if created:
                print(f'Group {group} created.')
                counter += 1
            else:  # pragma: no cover
                print(f'Group {group} already existing. Not creating.')
        print(f'Created {counter} groups.')
