# Fixtures are kept in dashboard/tests/conftest.py.
import pytest

from django.utils import timezone

from dashboard.tests.factories import SmileyFactory, OopsyFactory




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


@pytest.mark.django_db
def test_add_smiley_form_clean(instanced_form_with_new_description):
    """Confirms new description overrides description."""
    form = instanced_form_with_new_description
    assert form.clean() == {'description': 'New description',
                            'new_description': 'New description',
                            'points': 3}


@pytest.mark.django_db
def test_add_smiley_form_standard_choices(instanced_form_with_new_description):
    """Confirm standard choices are used for description field."""
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


@pytest.mark.django_db
def test_add_smiley_form_adds_choices(smiley_custom_description,
                                      instanced_form_with_new_description):
    """Check if new description is added to the description field's choices."""
    # Create Smiley object with a custom description.
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
                        'Removed cutlery from dishwasher'),
                       ('Removed rubbish',
                        'Removed rubbish')]


@pytest.mark.django_db
def test_add_smiley_form_adds_only_distinct_choices(smileys_with_same_description,
                                                    instanced_form_with_new_description):
    # Confirm that the new description is added to the description choices
    # only once (we have 5 Smiley objects from smileys_with_same_description
    # fixture and one from the form.
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
                        'Removed cutlery from dishwasher'),
                       ('Removed rubbish',
                        'Removed rubbish')]

# Tests for Oopsy forms.

@pytest.mark.django_db
def test_add_oopsy_form_with_valid_data(add_oopsy_form_set_description):
    form = add_oopsy_form_set_description
    assert form.is_valid() is True
    # Confirm manually set field attributes are ok.
    assert form.fields['description'].help_text == 'Required'
    assert form.fields['new_description'].help_text == (
        'Required, Create a new description')
    assert form.fields['points'].help_text == (
        'Required, How many points to take away?')