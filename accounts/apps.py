from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # noqa
        from core.permissions import GroupPermissionSetter
        group_permission_setter = GroupPermissionSetter
        post_migrate.connect(group_permission_setter.add_groups, sender=self)
        post_migrate.connect(group_permission_setter.add_app_permissions, sender=self)
