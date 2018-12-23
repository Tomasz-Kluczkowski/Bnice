"""
Support for declaring global groups, their per object permissions and any classes / functions needed for this purpose.
"""
from django.contrib.auth.models import Group
from django.template.defaultfilters import pluralize
from guardian.shortcuts import assign_perm


class GroupPermissionSetter:
    INSTANCE = 'instance'

    # Group keys
    PARENTS = 'Parents'

    # App keys
    ACCOUNTS = 'accounts'

    # Permission verb keys
    ADD = 'add'

    # Model keys
    USER = 'user'
    CHILD = 'child'

    GROUPS = [PARENTS]

    GROUP_PERMISSIONS = {
        ACCOUNTS: {
            PARENTS: {
                ADD: [USER, CHILD]
            }
        },
    }

    @classmethod
    def add_groups(cls, sender, **kwargs):
        """
        Add groups after migration. Use in accounts as it is first in migrations.

        Parameters
        ----------
        sender : AppConfig
            Signal sender. Application's configuration class.
        """

        print('Adding groups.')
        counter = 0
        for group in cls.GROUPS:
            group, created = Group.objects.get_or_create(name=group)
            if created:
                print(f"Group '{group}' created.")
                counter += 1
            else:
                print(f"Group '{group}' already existing. Not creating.")  # pragma: no cover
        print(f'Created {counter} group{pluralize(counter)}.')

    @classmethod
    def add_app_permissions(cls, sender, **kwargs):
        """
        Add application permissions to groups after app migration.
        Use the following hierarchy: app(dict) -> group(dict) -> verb(list(objects)).
        To be used in ready functions of application config classes.

        Parameters
        ----------
        sender : AppConfig
            Signal sender. Application's configuration class.
        """
        app = sender.name
        counter = 0
        app_permissions = cls.GROUP_PERMISSIONS[app]
        for group, verbs in app_permissions.items():
            print(f"Assigning '{app}' application's permissions for '{group}' group.")
            group = Group.objects.get(name=group)
            for verb, models in verbs.items():
                for model in models:
                    permission_code = ('_'.join([verb, model, cls.INSTANCE]))
                    assign_perm(f'{app}.{permission_code}', group)
                    print(f'Assigned permission: {app}.{permission_code}')
                    counter += 1
        print(f"{counter} '{app}' group permissions assigned.")
