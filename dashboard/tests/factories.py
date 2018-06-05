import factory
from dashboard.models import Smiley, Oopsy
from accounts.models import Child


class SmileyFactory(factory.DjangoModelFactory):
    """Generate Smiley objects."""

    class Meta:
        model = Smiley

    owner = factory.SubFactory(Child)


class OopsyFactory(factory.DjangoModelFactory):
    """Generate Oopsy objects."""

    class Meta:
        model = Oopsy

    owner = factory.SubFactory(Child)
