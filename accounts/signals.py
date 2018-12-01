from django.core.exceptions import SuspiciousOperation
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_object_permissions(sender, instance, created, **kwargs):
    """
    Adds per object permissions to the User instance after its creation.
    For new child users added by parents we need to add per object permissions to parent and child user so that both
    can access the object.
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
        if instance.is_parent() or instance.is_administrator():
            print('parent user')
        elif instance.is_child():
            assign_perm('accounts.view_user', instance, instance)
            assign_perm('accounts.edit_user', instance, instance)
            print('child user')

        print('User post save done')
        print(sender)
        print(instance)

    #
    # def post_save(self, *args, **kwargs):
    #     # Set per object permissions for user being saved.
    #     assign_perm('accounts.view_user', self, self)
    #     assign_perm('accounts.edit_user', self, self)
'''parent view, edit, delete'''
'''child view, edit'''