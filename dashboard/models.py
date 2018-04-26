from django.db import models
from django.conf import settings
from django.urls import reverse
from accounts.models import Child


# Create your models here.
class Action(models.Model):
    owner = models.ForeignKey(Child,
                              on_delete=models.CASCADE,
                              null=True)
    earned_on = models.DateField(blank=False)
    description = models.CharField(max_length=255, blank=False)
    points = models.IntegerField(default=3, blank=False)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(
            "dashboard:child_detail",
            kwargs={
                "parent": self.owner.parent,
                "child_username": self.owner.user.username,
                "pk": self.owner.pk,
            }
        )


class Smiley(Action):
    pass


class Oopsy(Action):
    pass


