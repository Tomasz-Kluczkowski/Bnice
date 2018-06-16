from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


class User(AbstractUser):
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, null=True)
    is_parent = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/%Y/%m/%d',
                                      blank=True)

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
    # Points required to be rewarded with a star.
    star_points = models.PositiveSmallIntegerField(blank=False, null=True)

    def get_absolute_url(self):
        return reverse(
            "dashboard:child_detail",
            kwargs={
                "parent": self.parent.username,
                "child_username": self.user.username,
                "pk": self.pk
            }
        )

    def __str__(self):
        return self.user.username
