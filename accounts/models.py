from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

from core.validators import ImageValidator


def get_anonymous_user_instance(user):
    return User(username=settings.ANONYMOUS_USER_NAME, email='anonymous@anonymous.anonymous')


class User(AbstractUser):
    TYPE_ADMIN = 'Administrator'
    TYPE_PARENT = 'Parent'
    TYPE_CHILD = 'Child'
    user_type = models.CharField(max_length=30, editable=False, null=True)
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    profile_photo = models.ImageField(
        upload_to='profiles/%Y/%m/%d',
        blank=True,
        validators=[
            ImageValidator(
                allowed_extensions=['.jpg', '.png', '.gif'],
                allowed_mimes=['image/jpeg', 'image/png', 'image/gif'],
                min_size=25,
                max_size=150,
                min_width=300,
                max_width=500,
                min_height=300,
                max_height=500
            )
        ]
    )

    class Meta:
        permissions = (
            ('view_user_instance', 'View User Instance'),
            ('add_user_instance', 'Add User Instance'),
            ('edit_user_instance', 'Edit User Instance'),
            ('delete_user_instance', 'Delete User Instance')
        )

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = self.TYPE_ADMIN
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def is_administrator(self):
        return self.user_type == self.TYPE_ADMIN

    def is_parent(self):
        return self.user_type == self.TYPE_PARENT

    def is_child(self):
        return self.user_type == self.TYPE_CHILD


class Child(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name="children")
    # Points required to be rewarded with a star.
    star_points = models.PositiveSmallIntegerField(blank=False, null=True)

    class Meta:
        permissions = (
            ('view_child_instance', 'View Child Instance'),
            ('add_child_instance', 'Add Child Instance'),
            ('edit_child_instance', 'Edit Child Instance'),
            ('delete_child_instance', 'Delete Child Instance')
        )

    def get_absolute_url(self):
        return reverse("dashboard:child-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.user.username
