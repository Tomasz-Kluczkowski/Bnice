from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm

from dashboard.models import (Smiley,
                              # Action
                              )


# def add_object_permissions(sender, instance, created, **kwargs):
#     """
#     Adds per object permissions when it is initially saved to the database.
#
#     Parameters
#     ----------
#     sender : Class
#         Class of the object that was saved.
#     instance : Any
#         Instance of the object that was saved.
#     created : Bool
#         If True instance was saved correctly.
#     """
#     pass
#     if issubclass(instance, Action):
#         parent_user = instance.owner.paret
#         child_user = instance.owner.user
#     # if created:


@receiver(post_save, sender=Smiley)
def add_smiley_object_permissions(sender, instance, created, **kwargs):
    """
    Adds per object permissions for parent and child users related to Smiley object instance after it was saved.

    Parameters
    ----------
    sender : Smiley
        Signal sender. Model of the object that was saved.
    instance : Smiley
        Instance of the Smiley object that was saved.
    created : Bool
        If True instance was saved correctly.
    """
    if created:
        parent_user = instance.owner.parent
        # common permissions
        assign_perm('dashboard.view_smiley_instance', parent_user, instance)
        assign_perm('dashboard.view_smiley_instance', instance.owner.user, instance)
        # parent_user permissions
        assign_perm('dashboard.edit_smiley_instance', parent_user, instance)
        assign_perm('dashboard.delete_smiley_instance', parent_user, instance)


@receiver(pre_delete, sender=Smiley)
def remove_smiley_object_permissions(sender, instance, **kwargs):
    """
    Removes all permissions associated with the smiley about to get deleted.

    Parameters
    ----------
    sender : Smiley
        Signal sender. Model of the object that is about to get deleted.
    instance : Smiley
        Instance of the Smiley object that we need to remove all permissions from.
    """
    filters = Q(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
