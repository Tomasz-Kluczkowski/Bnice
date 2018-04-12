from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Child(models.Model):
    name = models.CharField(max_length=255, blank=False)
    surname = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey(Parent,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name="children")

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Parent.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.parent.save()
