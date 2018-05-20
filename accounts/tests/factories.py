import factory
from accounts.models import User, Child


class UserFactory(factory.DjangoModelFactory):
    """Generate User objects."""

    class Meta:
        model = User


class ChildFactory(factory.DjangoModelFactory):
    """Generate Child objects."""

    class Meta:
        model = Child

    user = factory.SubFactory(UserFactory)
    parent = factory.SubFactory(UserFactory)
