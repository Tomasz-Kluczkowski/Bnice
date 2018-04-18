from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    name = models.CharField(max_length=30, blank=False)
    is_parent = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.username


class Child(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name="children")

    def __str__(self):
        return self.user.username
