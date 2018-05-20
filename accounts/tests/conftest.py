import pytest
from accounts.tests.factories import UserFactory, ChildFactory


@pytest.fixture()
def parent_user(db):
    create_parent_user = UserFactory(username='tom_k', name='Tom',
                                     email='tom@dot.pl', is_parent=True,
                                     is_child=False, profile_photo='')
    return create_parent_user


@pytest.fixture()
def child_user(db):
    create_child_user = UserFactory(username='nat_k', name='Natalie',
                                    email='nat@dot.pl', is_parent=False,
                                    is_child=True, profile_photo='')
    return create_child_user
