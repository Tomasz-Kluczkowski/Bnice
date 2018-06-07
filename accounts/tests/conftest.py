import pytest
from accounts.tests.factories import UserFactory, ChildFactory


@pytest.fixture()
def parent_user(db):
    """Creates a parent website user."""
    create_parent_user = UserFactory(username='tom_k', name='Tom',
                                     email='tom@dot.pl', is_parent=True,
                                     is_child=False, profile_photo='')
    return create_parent_user


@pytest.fixture()
def child_user(db):
    """Creates a child website user."""
    create_child_user = UserFactory(username='nat_k', name='Natalie',
                                    email='nat@dot.pl', is_parent=False,
                                    is_child=True, profile_photo='')
    return create_child_user


@pytest.fixture()
def child(db, child_user, parent_user):
    """Creates a Child object in the database."""
    child_obj = ChildFactory(user=child_user, parent=parent_user,
                             star_points=15)
    return child_obj
