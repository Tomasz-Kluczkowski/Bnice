"""
Support for declaring global groups, their per object permissions and any classes / functions needed for this purpose.
"""
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.template.defaultfilters import pluralize
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm

from dashboard.models import Action

INSTANCE = 'instance'

# Group keys
PARENTS = 'Parents'

# App keys
ACCOUNTS = 'accounts'
DASHBOARD = 'dashboard'

# Permission verb keys
ADD = 'add'
VIEW = 'view'
EDIT = 'edit'
DELETE = 'delete'

# Model keys
USER = 'user'
CHILD = 'child'
SMILEY = 'smiley'
OOPSY = 'oopsy'


class GroupPermissionSetter:
    """
    Helper class to be used to create groups and add their permissions.
    """
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
                    permission_code = ('_'.join([verb, model, INSTANCE]))
                    assign_perm(f'{app}.{permission_code}', group)
                    print(f'Assigned permission: {app}.{permission_code}')
                    counter += 1
        print(f"{counter} '{app}' group permissions assigned.")


class ObjectPermissionSetter:
    """
    Helper class to be used to add per object permissions.
    """
    CHILD_USER_VERBS = [VIEW]
    VERBS = [VIEW, EDIT, DELETE]

    def add_object_permissions(self, sender, instance, created, **kwargs):
        """
        Adds per object permissions for the parent and child users when object is initially saved to the database.

        Parameters
        ----------
        sender : Class
            Class of the object that was saved.
        instance : Any
            Instance of the object that was saved.
        created : Bool
            If True instance was saved correctly.
        """
        parent_user = None
        child_user = None
        if issubclass(sender, Action):
            parent_user = instance.owner.parent
            child_user = instance.owner.user
        if created:
            ct = ContentType.objects.get_for_model(instance)
            app = ct.app_label
            model = ct.model
            # add parent user permissions.
            for verb in self.VERBS:
                permission_code = ('_'.join([verb, model, INSTANCE]))
                assign_perm(f'{app}.{permission_code}', parent_user, instance)
                if verb in self.CHILD_USER_VERBS:
                    # add child user permissions.
                    assign_perm(f'{app}.{permission_code}', child_user, instance)

    def remove_object_permissions(self, sender, instance, **kwargs):
        """
        Removes all permissions associated with the object about to get deleted.

        Parameters
        ----------
        sender : Class
            Signal sender. Class of the object that is about to get deleted.
        instance : Any
            Instance of the object that we need to remove all permissions from.
        """
        filters = Q(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
        UserObjectPermission.objects.filter(filters).delete()
