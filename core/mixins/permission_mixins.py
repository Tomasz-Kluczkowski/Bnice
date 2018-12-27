# Permission mixins to override default django-guardian behaviour
from guardian.mixins import PermissionRequiredMixin


class SetChildPermissionObjectMixin:
    """
    Sets child object as the focus of the permission check in the view.
    """
    def get_permission_object(self):
        return self.child


class PermissionRequired403Mixin(PermissionRequiredMixin):
    """
    Basic PermissionRequired mixin to use in views.

    Forces 403 http error on failed permission check.
    """
    return_403 = True


class PermissionRequired403GlobalMixin(PermissionRequiredMixin):
    """
    Basic Global PermissionRequired mixin to use in views.

    Forces 403 http error on failed permission check. Disables permission object (only global check is made for User
    instance)
    """
    return_403 = True
    accept_global_perms = True
    permission_object = None


class PermissionRequiredSetChild403Mixin(SetChildPermissionObjectMixin, PermissionRequired403Mixin):
    """
    PermissionRequired mixin to be used in views when we have to provide child object as the one for which we want to
    check the permission for (i.e. AddSmiley / EditChild where the view object is a Smiley / User but check has to be
    made for Child.
    """
    pass
