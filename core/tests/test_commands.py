import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command

from core.permissions import GroupPermissionSetter

pytestmark = pytest.mark.django_db


def test_add_groups_command():
    Group.objects.all().delete()
    call_command('add_groups')
    assert Group.objects.count() == len(GroupPermissionSetter.GROUPS)


def test_add_permissions_command(parent_user):
    Group.objects.all().delete()
    call_command('add_groups')
    parents = Group.objects.get(name='Parents')
    parent_user.groups.add(parents)
    call_command('add_group_permissions')
    assert parents.permissions.count() == 2
    assert parent_user.has_perm('accounts.add_user_instance')
    assert parent_user.has_perm('accounts.add_child_instance')
