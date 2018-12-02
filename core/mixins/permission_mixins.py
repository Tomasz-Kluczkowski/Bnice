# Permission mixins to override default django-guardian behaviour
from guardian.mixins import PermissionRequiredMixin


class PermissionRequiredMixin403(PermissionRequiredMixin):
    return_403 = True
