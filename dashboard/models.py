from django.db import models
from django.urls import reverse
from accounts.models import Child


# Create your models here.
class Action(models.Model):
    """Saves actions.

    This model will save child's actions for which they earn points.
    Claimed field will be set to True when child reaches enough points to
    get a star. This field is intended to never be shown to the user.
    """
    earned_on = models.DateTimeField(blank=False)
    claimed = models.BooleanField(default=False)
    points_remaining = models.PositiveSmallIntegerField(default=0)
    description = models.CharField(max_length=255, blank=False)
    points = models.IntegerField(default=3, blank=False)

    class Meta:
        abstract = True
        ordering = ['earned_on']

    def get_absolute_url(self):
        return reverse("dashboard:child-detail", kwargs={"pk": self.owner.pk})

    def __str__(self):
        return self.description


class Smiley(Action):
    owner = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='smileys')
    star_awarded = models.BooleanField(default=False)


class Oopsy(Action):
    owner = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='oopsies')
