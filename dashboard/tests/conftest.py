import pytest
from django.utils import timezone

from dashboard.forms import AddSmileyForm, AddOopsyForm
from dashboard.tests.factories import SmileyFactory, OopsyFactory
# Imports of fixtures will show as unused.
from accounts.tests.conftest import (child, child_user, parent_user,
                                     parent_user_password)


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
def smiley_form_new_description_saved(add_smiley_form_new_description, child):
    """Returns a saved instance of the form with a new description."""
    form = add_smiley_form_new_description
    obj = form.save(commit=False)
    obj.owner = child
    current_time = timezone.now()
    obj.earned_on = current_time
    # Save object to the database
    form.save()
    return form


@pytest.fixture
def smiley_custom_description(child):
    """Return a Smiley object with a custom description."""
    custom_smiley = SmileyFactory(owner=child,
                                  earned_on=timezone.now(),
                                  description="Removed rubbish",
                                  points=5)
    custom_smiley.save()
    return custom_smiley


@pytest.fixture
def smileys_with_same_description(child):
    # Create 5 Smiley objects with the same description.
    for i in range(5):
        custom_smiley = SmileyFactory(owner=child,
                                      earned_on=timezone.now(),
                                      description="Removed rubbish",
                                      points=5)
        custom_smiley.save()


# Oopsy form fixtures.


@pytest.fixture
def add_oopsy_form_set_description():
    """Returns an instance of AddSmileyForm with a description from one of the
    choices."""
    form = AddOopsyForm({'description': 'Left mess',
                         'new_description': '',
                         'points': 3})
    return form


@pytest.fixture
def add_oopsy_form_new_description():
    """Returns an instance of AddOopsyForm with a new, custom description."""
    form = AddOopsyForm({'description': 'Add new',
                         'new_description': 'New description',
                         'points': 3})
    return form


@pytest.fixture
def oopsy_form_new_description_saved(add_oopsy_form_new_description, child):
    """Returns a saved instance of the form with a new description."""
    form = add_oopsy_form_new_description
    obj = form.save(commit=False)
    obj.owner = child
    current_time = timezone.now()
    obj.earned_on = current_time
    # Save object to the database
    form.save()
    return form


@pytest.fixture
def oopsy_custom_description(child):
    """Return an Oopsy object with a custom description."""
    custom_oopsy = OopsyFactory(owner=child,
                                earned_on=timezone.now(),
                                description='Was rude',
                                points=5)
    custom_oopsy.save()
    return custom_oopsy


@pytest.fixture
def oopsies_with_same_description(child):
    """Create 5 Oopsy objects with the same description."""
    for i in range(5):
        custom_oopsy = OopsyFactory(owner=child,
                                    earned_on=timezone.now(),
                                    description='Was rude',
                                    points=5)
        custom_oopsy.save()
