from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # noqa
        from core.permissions import GroupPermissionSetter
        group_adder = GroupPermissionSetter
        post_migrate.connect(group_adder.add_groups, sender=self)
        post_migrate.connect(group_adder.add_app_permissions, sender=self)
