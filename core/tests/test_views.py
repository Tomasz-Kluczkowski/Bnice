import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_url_for_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_url_reverse_for_home_page(client):
    response = client.get(reverse('core:home'))
    assert response.status_code == 200


def test_home_page_view_uses_correct_template(client):
    response = client.get(reverse('core:home'))
    templates = response.templates
    assert templates[0].name == 'core/index.html'
