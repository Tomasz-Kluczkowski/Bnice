# Fixtures are kept in dashboard/tests/conftest.py.
import pytest
from dashboard.models import Oopsy, Smiley


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
def test_add_smiley_form_clean(smiley_form_new_description_saved):
    """Confirms new description overrides description."""
    form = smiley_form_new_description_saved
    assert form.clean() == {'description': 'New description',
                            'new_description': 'New description',
                            'points': 3}


@pytest.mark.django_db
def test_add_smiley_form_standard_choices(smiley_form_new_description_saved):
    """Confirm standard choices are used for description field."""
    form = smiley_form_new_description_saved
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
                                      smiley_form_new_description_saved):
    """Check if new description is added to the description field's choices."""
    # Create Smiley object with a custom description.
    form = smiley_form_new_description_saved
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
def test_add_smiley_form_adds_only_distinct_choices(
        smileys_with_same_description,
        smiley_form_new_description_saved):
    # Confirm that the new description is added to the description choices
    # only once (we have 5 Smiley objects from smileys_with_same_description
    # fixture and one from the form.
    form = smiley_form_new_description_saved
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
    assert Smiley.objects.count() == 6


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


@pytest.mark.django_db
def test_add_oopsy_form_clean(oopsy_form_new_description_saved):
    """Confirms new description overrides description."""
    form = oopsy_form_new_description_saved
    assert form.clean() == {'description': 'New description',
                            'new_description': 'New description',
                            'points': 3}


@pytest.mark.django_db
def test_add_oopsy_form_standard_choices(oopsy_form_new_description_saved):
    """Confirm standard choices are used for description field."""
    form = oopsy_form_new_description_saved
    choices = form.fields['description'].choices
    assert choices == [('Add new',
                        'Add new'),
                       ('Was lying',
                        'Was lying'),
                       ('Left mess',
                        'Left mess'),
                       ('Talked back to parent',
                        'Talked back to parent'),
                       ("Didn't do homework",
                        "Didn't do homework")]


@pytest.mark.django_db
def test_add_oopsy_form_adds_choices(oopsy_custom_description,
                                     oopsy_form_new_description_saved):
    """Check if new description is added to the description field's choices."""
    # Create Smiley object with a custom description.
    form = oopsy_form_new_description_saved
    choices = form.fields['description'].choices
    assert choices == [('Add new',
                        'Add new'),
                       ('Was lying',
                        'Was lying'),
                       ('Left mess',
                        'Left mess'),
                       ('Talked back to parent',
                        'Talked back to parent'),
                       ("Didn't do homework",
                        "Didn't do homework"),
                       ('Was rude',
                        'Was rude')]


@pytest.mark.django_db
def test_add_oopsy_form_adds_only_distinct_choices(
        oopsies_with_same_description,
        oopsy_form_new_description_saved):
    # Confirm that the new description is added to the description choices
    # only once (we have 5 Oopsy objects from oopsies_with_same_description
    # fixture and one from the form.
    form = oopsy_form_new_description_saved
    choices = form.fields['description'].choices
    assert choices == [('Add new',
                        'Add new'),
                       ('Was lying',
                        'Was lying'),
                       ('Left mess',
                        'Left mess'),
                       ('Talked back to parent',
                        'Talked back to parent'),
                       ("Didn't do homework",
                        "Didn't do homework"),
                       ('Was rude',
                        'Was rude')]
    assert Oopsy.objects.count() == 6
