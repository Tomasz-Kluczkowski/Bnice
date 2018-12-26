from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from Bnice import settings
from accounts.models import Child
from core.permissions import ObjectPermissionSetter


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_object_permissions(sender, instance, created, **kwargs):
    """
    Adds per object permissions to the User instance after its creation. Django guardian adds anonymous user before
    permissions get created in the database so we have to eliminate triggering signal for that (as per django guardian
    docs).

    Parameters
    ----------
    sender : User
        Signal sender. Model of the object that was saved.
    instance : User
        Instance of the User object that was saved to which we add permissions.
    created : Bool
        If True instance was saved correctly.
    """
    if created and instance.username != settings.ANONYMOUS_USER_NAME:
        # common permissions
        assign_perm('accounts.view_user_instance', instance, instance)
        assign_perm('accounts.edit_user_instance', instance, instance)
        if instance.is_parent() or instance.is_administrator():
            parents = Group.objects.get(name='Parents')
            instance.groups.add(parents)
            assign_perm('accounts.delete_user_instance', instance, instance)


object_permission_setter = ObjectPermissionSetter()
pre_delete.connect(object_permission_setter.remove_object_permissions, sender=settings.AUTH_USER_MODEL)
post_save.connect(object_permission_setter.add_object_permissions, sender=Child)
pre_delete.connect(object_permission_setter.remove_object_permissions, sender=Child)


@receiver(post_delete, sender=Child)
def delete_related_child_user(sender, instance, **kwargs):
    """
    Deletes related user (foreign key) after Child instance was deleted.

    Parameters
    ----------
    sender : Child
        Signal sender. Model of the object that was deleted.
    instance : Child
        Instance of the Child object that was deleted.
    """
    if instance.user:
        instance.user.delete()
