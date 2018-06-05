import pytest

from dashboard.forms import AddSmileyForm, AddOopsyForm


@pytest.fixture
def add_smiley_form_with_set_description():
    """Returns an instance of AddSmileyForm with a description from one of the
    choices."""
    form = AddSmileyForm({'description': 'Folded washing',
                          'new_description': '',
                          'points': 3})
    return form


@pytest.mark.django_db
def test_add_smiley_form_with_valid_data(add_smiley_form_with_set_description):
    form = add_smiley_form_with_set_description
    assert form.is_valid() is True
    # Confirm manually set field attributes are ok.
    assert form.fields['description'].help_text == 'Required'
    assert form.fields['new_description'].help_text == (
        'Required, Create a new description')
    assert form.fields['points'].help_text == (
        'Required, How much was this task worth?')

@pytest.mark.django_db
def



