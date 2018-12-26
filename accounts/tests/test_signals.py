from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.models import UserObjectPermission

from Bnice import settings
from accounts.models import User


class TestUserSignals:

    def test_add_user_object_permissions_parent_user(self, parent_user):
        assert parent_user.has_perm('accounts.view_user_instance', parent_user)
        assert parent_user.has_perm('accounts.edit_user_instance', parent_user)
        assert parent_user.has_perm('accounts.add_user_instance')
        assert parent_user.has_perm('accounts.delete_user_instance', parent_user)

    def test_add_user_object_permissions_admin_user(self, admin_user):
        assert admin_user.has_perm('accounts.view_user_instance', admin_user)
        assert admin_user.has_perm('accounts.edit_user_instance', admin_user)
        assert admin_user.has_perm('accounts.add_user_instance')
        assert admin_user.has_perm('accounts.delete_user_instance', admin_user)

    def test_add_user_object_permissions_child_user(self, child_user):
        assert child_user.has_perm('accounts.view_user_instance', child_user)
        assert child_user.has_perm('accounts.edit_user_instance', child_user)
        assert not child_user.has_perm('accounts.add_user_instance')
        assert not child_user.has_perm('accounts.delete_user_instance', child_user)

    def test_user_object_permissions_removed_after_user_deleted(self, parent_user):
        filters = Q(content_type=ContentType.objects.get_for_model(parent_user), object_pk=parent_user.pk)
        parent_user.delete()
        assert not UserObjectPermission.objects.filter(filters).exists()


class TestChildSignals:

    def test_add_child_object_permissions_parent_user(self, parent_user, child):
        assert parent_user.has_perm('accounts.view_child_instance', child)
        assert parent_user.has_perm('accounts.edit_child_instance', child)
        assert parent_user.has_perm('accounts.delete_child_instance', child)

    def test_add_child_object_permissions_child_user(self, parent_user, child, child_user):
        assert child_user.has_perm('accounts.view_child_instance', child)
        assert not child_user.has_perm('accounts.edit_child_instance', child)
        assert not child_user.has_perm('accounts.delete_child_instance', child)

    def test_child_object_permissions_removed_after_child_deleted(self, parent_user, child):
        assert parent_user.has_perm('accounts.view_child_instance', child)
        filters = Q(content_type=ContentType.objects.get_for_model(child),
                    object_pk=child.pk)
        child.delete()
        assert not UserObjectPermission.objects.filter(filters).exists()

    def test_child_user_deleted_after_child_deleted(self, child, child_user):
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 2
        child.delete()
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 1
