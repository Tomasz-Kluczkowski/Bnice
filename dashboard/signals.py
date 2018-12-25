from django.db.models.signals import post_save, pre_delete

from dashboard.models import Smiley, Oopsy
from core.permissions import ObjectPermissionSetter


object_permission_setter = ObjectPermissionSetter()
models = [Oopsy, Smiley]


for model in models:
    post_save.connect(object_permission_setter.add_object_permissions, sender=model)
    pre_delete.connect(object_permission_setter.remove_object_permissions, sender=model)
