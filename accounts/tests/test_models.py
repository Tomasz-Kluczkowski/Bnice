import pytest
from accounts.models import User, Child
from accounts.tests.factories import ChildFactory


def test_user_model(parent_user):
    assert isinstance(parent_user, User)
    assert parent_user.__str__() == parent_user.username
    assert User.objects.count() == 1
    assert parent_user.username == 'tom_k'
    assert parent_user.name == 'Tom'
    assert parent_user.email == 'tom@dot.pl'
    assert parent_user.profile_photo == ''
    assert parent_user.user_type == User.TYPE_PARENT


@pytest.mark.django_db
def test_child_model(parent_user, child_user):
    child = ChildFactory(user=child_user, parent=parent_user, star_points=15)
    assert isinstance(child, Child)
    assert child.__str__() == child.user.username
    assert child.get_absolute_url() == (
        '/dashboard/child/{0}/'.format(child.pk))
    assert User.objects.count() == 2
    assert child.user.username == 'nat_k'
    assert child.user.name == 'Natalie'
    assert child.user.email == 'nat@dot.pl'
    assert child.user.user_type == User.TYPE_CHILD
    assert child.star_points == 15
    assert child.parent.username == 'tom_k'


@pytest.mark.django_db
def test_superuser_is_administrator():
    password = 'password'
    admin = User.objects.create_superuser('admin_man', 'myemail@test.com',
                                          password)
    assert admin.is_administrator()
