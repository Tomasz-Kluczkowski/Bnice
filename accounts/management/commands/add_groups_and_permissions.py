from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm

GLOBAL_PERMISSIONS = [
    'accounts.add_user_instance',
    'accounts.add_child_instance',
    'dashboard.add_smiley_instance',
    'dashboard.add_oopsy_instance'
]


class Command(BaseCommand):
    """
    Use to add all necessary groups and their global permissions here.
    """
    help = 'Add groups and global permissions to them.'

    def handle(self, *args, **kwargs):
        parents, created = Group.objects.get_or_create(name='Parents')
        if created:
            self.stdout.write(self.style.SUCCESS('Group Parents created.'))
            print('Assigning permissions.')
            for permission in GLOBAL_PERMISSIONS:
                assign_perm(permission, parents)
                print(f'Assigned {permission} permission to group {parents}.')
            self.stdout.write(self.style.SUCCESS('All permissions assigned.'))
        else:
            self.stdout.write(self.style.SUCCESS('Group Parents already existing. Not creating.'))

