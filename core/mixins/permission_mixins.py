# Permission mixins to override default django-guardian behaviour
from django.shortcuts import get_object_or_404
from guardian.mixins import PermissionRequiredMixin

from accounts.models import Child


class SetChildPermissionObjectMixin:
    """
    Adds child attribute to the view which is needed for the permission check and view logic.
    """
    def dispatch(self, request, *args, **kwargs):
        self.child = get_object_or_404(Child.objects, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_permission_object(self):
        return self.child


class PermissionRequired403Mixin(PermissionRequiredMixin):
    """
    Basic PermissionRequired mixin to use in views.
    """
    return_403 = True


class PermissionRequiredSetChild403Mixin(SetChildPermissionObjectMixin, PermissionRequired403Mixin):
    """
    PermissionRequired mixin to be used in views when we have to provide child object as the one for which we want to
    check the permission for (i.e. AddSmiley / EditChild where the view object is a Smiley / User but check has to be
    made for Child.
    """
    pass
