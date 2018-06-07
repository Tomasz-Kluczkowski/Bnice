import pytest
from django.utils import timezone

from dashboard.forms import AddSmileyForm, AddOopsyForm
from dashboard.models import Smiley, Oopsy


@pytest.fixture
def add_smiley_form_set_description():
    """Returns an instance of AddSmileyForm with a description from one of the
    choices."""
    form = AddSmileyForm({'description': 'Folded washing',
                          'new_description': '',
                          'points': 3})
    return form


@pytest.fixture
def add_smiley_form_new_description():
    """Returns an instance of AddSmileyForm with a new, custom description."""
    form = AddSmileyForm({'description': 'Add new',
                          'new_description': 'New description',
                          'points': 3})
    return form


@pytest.fixture
def instanced_form_with_new_description(add_smiley_form_new_description, child):
    """Returns a saved instance of the form with a new description."""
    form = add_smiley_form_new_description
    obj = form.save(commit=False)
    obj.owner = child
    current_time = timezone.now()
    obj.earned_on = current_time
    # Save object to the database
    form.save()
    return form


@pytest.mark.django_db
def test_add_smiley_form_with_valid_data(add_smiley_form_set_description):
    form = add_smiley_form_set_description
    assert form.is_valid() is True
    # Confirm manually set field attributes are ok.
    assert form.fields['description'].help_text == 'Required'
    assert form.fields['new_description'].help_text == (
        'Required, Create a new description')
    assert form.fields['points'].help_text == (
        'Required, How much was this task worth?')

# @pytest.mark.django_db
# def test_add_smiley_form_with_new_description(
#         add_smiley_form_new_description, child):
#     form = add_smiley_form_new_description
#     obj = form.save(commit=False)
#     obj.owner = child
#     current_time = timezone.now()
#     obj.earned_on = current_time
#     # Save object to the database
#     assert form.clean() == 'New description'
#     form.save()
#     assert form.is_valid() is True
#     smiley = Smiley.objects.get(id=1)
#     # assert smiley.description == 'New description'


@pytest.mark.django_db
def test_add_smiley_form_clean(instanced_form_with_new_description):
    """Confirms new description overrides description."""
    form = instanced_form_with_new_description
    assert form.clean() == {'description': 'New description',
                            'new_description': 'New description',
                            'points': 3}


@pytest.mark.django_db
def test_add_smiley_standard_choices(instanced_form_with_new_description):
    form = instanced_form_with_new_description
    choices = form.fields['description'].choices
    assert choices == [('Add new',
                        'Add new'),
                       ('Folded washing',
                        'Folded washing'),
                       ('Cleaned bathroom',
                        'Cleaned bathroom'),
                       ('Mopped floor',
                        'Mopped floor'),
                       ('Removed cutlery from dishwasher',
                        'Removed cutlery from dishwasher')]





