from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from accounts.permissions import GROUPS


class Command(BaseCommand):
    """
    Use to add all necessary groups.
    """
    help = 'Add groups in the database.'

    def handle(self, *args, **kwargs):
        print('Running add_groups.')
        for group in GROUPS:
            group, created = Group.objects.get_or_create(name=group)
            if created:
                print(f'Group {group} created.')
            else:
                print(f'Group {group} already existing. Not creating.')
