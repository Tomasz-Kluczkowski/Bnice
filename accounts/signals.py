from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from guardian.models import UserObjectPermission, GroupObjectPermission
from guardian.shortcuts import assign_perm

from Bnice import settings
from accounts.models import Child


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
            assign_perm('accounts.add_user_instance', instance, instance)
            assign_perm('accounts.delete_user_instance', instance, instance)


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_user_object_permissions(sender, instance, **kwargs):
    """
    Removes all permissions associated with the user about to get deleted.

    Parameters
    ----------
    sender : User
        Signal sender. Model of the object that is about to get deleted.
    instance : User
        Instance of the User object that we need to remove all permissions from.
    """
    filters = Q(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()


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
