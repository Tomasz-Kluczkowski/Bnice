import pytest

from accounts.models import User, Child
from accounts.forms import UserCreateForm, ChildCreateForm


@pytest.mark.django_db
def test_user_create_form():
    form = UserCreateForm({'username': 'tom_k',
                           'email': 'tom@dot.pl',
                           'profile_photo': '',
                           'password1': 'pass123password',
                           'password2': 'pass123password'})
    assert form.is_valid() is True
    # Confirm manually set field attributes are ok.
    assert form.fields['password1'].help_text == (
        '8 characters or more & not numerical only.')
    assert form.fields['email'].required is True
    assert form.fields['email'].help_text == 'Required'
    assert form.fields['profile_photo'].help_text == (
        'Image file, size: 500x500 px, jpeg, png or gif type only.')
    user = form.save()
    # Confirm saved user matches data from form.
    assert user.username == 'tom_k'
    assert user.email == 'tom@dot.pl'
    assert user.profile_photo == ''
    # Confirm is_parent is appropriately set in save method.
    assert user.is_parent is True
    assert user.is_child is False


@pytest.mark.django_db
def test_child_create_form(parent_user):
    form = ChildCreateForm({'username': 'nat_k',
                            'email': 'nat@dot.pl',
                            'name': 'Natalie',
                            'star_points': 10,
                            'profile_photo': '',
                            'password1': 'pass123password',
                            'password2': 'pass123password',
                            },
                           initial={'current_user': parent_user})
    assert form.is_valid() is True
    # Confirm manually set field attributes are ok.
    assert form.fields['password1'].help_text == (
        '8 characters or more & not numerical only.')
    assert form.fields['email'].required is True
    assert form.fields['email'].help_text == 'Required'
    assert form.fields['profile_photo'].help_text == (
        'Image file, size: 500x500 px, jpeg, png or gif type only.')
    child_user = form.save()
    # Confirm saved child user matches data from form.
    assert child_user.username == 'nat_k'
    assert child_user.email == 'nat@dot.pl'
    assert child_user.name == 'Natalie'
    assert child_user.profile_photo == ''
    # Confirm is_child is appropriately set in save method.
    assert child_user.is_parent is False
    assert child_user.is_child is True
    child = Child.objects.get(user=child_user)
    # Confirm a new child object is created when a child user is saved.
    assert child.star_points == 10
    assert child.parent == parent_user
