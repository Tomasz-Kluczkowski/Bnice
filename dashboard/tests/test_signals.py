from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from guardian.models import UserObjectPermission


class TestSmileySignals:

    def test_add_smiley_object_permissions_parent_user(self, parent_user, child, smiley_custom_description):
        assert parent_user.has_perm('dashboard.view_smiley_instance', smiley_custom_description)
        assert parent_user.has_perm('dashboard.edit_smiley_instance', smiley_custom_description)
        assert parent_user.has_perm('dashboard.delete_smiley_instance', smiley_custom_description)

    def test_add_smiley_object_permissions_child_user(self, parent_user, child, child_user, smiley_custom_description):
        assert child_user.has_perm('dashboard.view_smiley_instance', smiley_custom_description)
        assert not child_user.has_perm('dashboard.edit_smiley_instance', smiley_custom_description)
        assert not child_user.has_perm('dashboard.delete_smiley_instance', smiley_custom_description)

    def test_smiley_object_permissions_removed_after_smiley_deleted(self, parent_user, child,
                                                                    smiley_custom_description):
        assert parent_user.has_perm('dashboard.view_smiley_instance', smiley_custom_description)
        filters = Q(content_type=ContentType.objects.get_for_model(smiley_custom_description),
                    object_pk=smiley_custom_description.pk)
        smiley_custom_description.delete()
        assert not UserObjectPermission.objects.filter(filters).exists()


class TestOopsySignals:

    def test_add_oopsy_object_permissions_parent_user(self, parent_user, child, oopsy_custom_description):
        assert parent_user.has_perm('dashboard.view_oopsy_instance', oopsy_custom_description)
        assert parent_user.has_perm('dashboard.edit_oopsy_instance', oopsy_custom_description)
        assert parent_user.has_perm('dashboard.delete_oopsy_instance', oopsy_custom_description)

    def test_add_oopsy_object_permissions_child_user(self, parent_user, child, child_user, oopsy_custom_description):
        assert child_user.has_perm('dashboard.view_oopsy_instance', oopsy_custom_description)
        assert not child_user.has_perm('dashboard.edit_oopsy_instance', oopsy_custom_description)
        assert not child_user.has_perm('dashboard.delete_oopsy_instance', oopsy_custom_description)

    def test_oopsy_object_permissions_removed_after_oopsy_deleted(self, parent_user, child, oopsy_custom_description):
        assert parent_user.has_perm('dashboard.view_oopsy_instance', oopsy_custom_description)
        filters = Q(content_type=ContentType.objects.get_for_model(oopsy_custom_description),
                    object_pk=oopsy_custom_description.pk)
        oopsy_custom_description.delete()
        assert not UserObjectPermission.objects.filter(filters).exists()
