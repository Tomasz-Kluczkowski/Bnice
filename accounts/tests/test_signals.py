from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.models import UserObjectPermission

from accounts.models import User


class TestUserSignals:

    def test_parent_user_post_save_signal(self, parent_user):
        """Make sure all permissions are correctly assigned to the new parent user instance."""
        user = parent_user
        assert user.has_perm('accounts.view_user_instance', user)
        assert user.has_perm('accounts.edit_user_instance', user)
        assert user.has_perm('accounts.add_user_instance')
        assert user.has_perm('accounts.delete_user_instance', user)

    def test_administrator_user_post_save_signal(self, admin_user):
        """Make sure all permissions are correctly assigned to the new administrator user instance."""
        user = admin_user
        assert user.has_perm('accounts.view_user_instance', user)
        assert user.has_perm('accounts.edit_user_instance', user)
        assert user.has_perm('accounts.add_user_instance')
        assert user.has_perm('accounts.delete_user_instance', user)

    def test_child_user_post_save_signal(self, child_user):
        """Make sure all permissions are correctly assigned to the new child user instance."""
        user = child_user
        assert user.has_perm('accounts.view_user_instance', user)
        assert user.has_perm('accounts.edit_user_instance', user)
        assert not user.has_perm('accounts.add_user_instance')
        assert not user.has_perm('accounts.delete_user_instance', user)

    def test_user_permissions_removed_after_user_deleted(self, parent_user):
        user = parent_user
        filters = Q(content_type=ContentType.objects.get_for_model(parent_user), object_pk=parent_user.pk)
        user.delete()
        assert not UserObjectPermission.objects.filter(filters).exists()

    def test_related_child_user_deleted_when_child_instance_deleted(self, child):
        child_user_pk = child.user.pk
        child.delete()
        assert not User.objects.filter(pk=child_user_pk).exists()
