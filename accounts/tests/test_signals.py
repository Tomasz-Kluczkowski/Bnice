import pytest

from accounts.models import User

pytestmark = pytest.mark.django_db


class TestUserPostSaveSignal:

    def test_parent_user_post_save_signal(self):
        """Make sure all permissions are correctly assigned to the new parent user instance."""
        user = User.objects.create(
            username='test_username',
            name='test_name',
            email='test_email@example.com',
            profile_photo='',
            user_type=User.TYPE_PARENT
        )
        assert user.has_perm('accounts.view_user_instance', user)
        assert user.has_perm('accounts.edit_user_instance', user)
        assert user.has_perm('accounts.add_user_instance', user)
        assert user.has_perm('accounts.delete_user_instance', user)

    def test_administrator_user_post_save_signal(self):
        """Make sure all permissions are correctly assigned to the new administrator user instance."""
        user = User.objects.create(
            username='test_username',
            name='test_name',
            email='test_email@example.com',
            profile_photo='',
            user_type=User.TYPE_ADMIN
        )
        assert user.has_perm('accounts.view_user_instance', user)
        assert user.has_perm('accounts.edit_user_instance', user)
        assert user.has_perm('accounts.add_user_instance', user)
        assert user.has_perm('accounts.delete_user_instance', user)

    def test_child_user_post_save_signal(self):
        """Make sure all permissions are correctly assigned to the new child user instance."""
        user = User.objects.create(
            username='test_username',
            name='test_name',
            email='test_email@example.com',
            profile_photo='',
            user_type=User.TYPE_CHILD
        )
        assert user.has_perm('accounts.view_user_instance', user)
        assert user.has_perm('accounts.edit_user_instance', user)
        assert not user.has_perm('accounts.add_user_instance', user)
        assert not user.has_perm('accounts.delete_user_instance', user)

