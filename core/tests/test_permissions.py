import pytest
from django.contrib.auth.models import Group

from accounts.apps import AccountsConfig
from core.permissions import GroupPermissionSetter

pytestmark = pytest.mark.django_db


class TestGroupPermissionSetter:
    group_perms_setter = GroupPermissionSetter

    def test_add_groups(self):
        Group.objects.all().delete()
        self.group_perms_setter.add_groups(AccountsConfig)
        assert Group.objects.count() == len(GroupPermissionSetter.GROUPS)

    def test_add_accounts_app_permissions(self, parent_user):
        Group.objects.all().delete()
        self.group_perms_setter.add_groups(AccountsConfig)
        parents = Group.objects.get(name='Parents')
        parent_user.groups.add(parents)
        self.group_perms_setter.add_app_permissions(AccountsConfig)
        assert parents.permissions.count() == 2
        assert parent_user.has_perm('accounts.add_user_instance')
        assert parent_user.has_perm('accounts.add_child_instance')
