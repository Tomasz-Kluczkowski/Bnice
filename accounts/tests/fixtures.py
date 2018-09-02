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
    """Creates a parent website user with a password."""
    user = parent_user
    user.set_password('password')
    user.save()
    return user


@pytest.fixture()
def alt_parent_user_password(db):
    """Creates an alt parent website user with a password.

    This will be used as an alternative parent user to confirm only children
    of currently logged in parent are shown in views.
    """

    user = UserFactory(username='johny_c', name='Johny',
                       email='johny@dot.pl', is_parent=True,
                       is_child=False, profile_photo='')
    user.set_password('password')
    user.save()
    return user


@pytest.fixture()
def child_user(db):
    """Creates a child website user."""
    user = UserFactory(username='nat_k', name='Natalie',
                       email='nat@dot.pl', is_parent=False,
                       is_child=True, profile_photo='')
    return user


@pytest.fixture()
def child_user_password(db, child_user):
    """Creates a child website user with a password."""
    print('in fixture')
    user = child_user
    user.set_password('password')
    user.save()
    return user


@pytest.fixture()
def alt_child_user(db):
    """Creates alternate child website user."""
    user = UserFactory(username='sophie_m', name='Sophie',
                       email='sm@dot.pl', is_parent=False,
                       is_child=True, profile_photo='')
    return user


@pytest.fixture()
def child(db, child_user, parent_user):
    """Creates a Child object in the database."""
    child_obj = ChildFactory(user=child_user, parent=parent_user,
                             star_points=15)
    return child_obj


@pytest.fixture()
def alt_child(db, alt_child_user, alt_parent_user_password):
    """Creates a Child object with an alt parent."""
    child_obj = ChildFactory(user=alt_child_user,
                             parent=alt_parent_user_password,
                             star_points=15)
    return child_obj
