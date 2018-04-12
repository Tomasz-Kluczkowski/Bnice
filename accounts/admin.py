from django.contrib import admin
from accounts import models

# Register your models here.
admin.site.register(models.Child)
admin.site.register(models.Parent)