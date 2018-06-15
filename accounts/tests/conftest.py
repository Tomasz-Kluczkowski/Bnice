import pytest
from accounts.tests.factories import UserFactory, ChildFactory


@pytest.fixture()
def parent_user(db):
    """Creates a parent website user."""
    user = UserFactory(username='tom_k', name='Tom',
                       email='tom@dot.pl', is_parent=True,
                       is_child=False, profile_photo='')
    return user


@pytest.fixture()
def parent_user_password(db, parent_user):
    """Creates a parent website user with password."""
    user = parent_user
    user.set_password('password')
    user.save()


@pytest.fixture()
def alt_parent_user_password(db):
    """Creates an alt parent website user with password."""
    user = UserFactory(username='johny_c', name='Johny',
                       email='johny@dot.pl', is_parent=True,
                       is_child=False, profile_photo='')
    user.set_password('password')
    user.save()


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
