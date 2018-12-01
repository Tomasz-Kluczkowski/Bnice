from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from Bnice import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_object_permissions(sender, instance, created, **kwargs):
    """
    Adds per object permissions to the User instance after its creation.
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

        print('User post save done')
        print(sender)
        print(instance)
