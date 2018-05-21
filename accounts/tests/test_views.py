import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_url_for_signup_page(client):
        response = client.get('/accounts/signup/')
        assert response.status_code == 200


def test_url_reverse_name_for_signup_page(client):
    response = client.get(reverse('accounts:signup'))
    assert response.status_code == 200


def test_signup_view_uses_correct_template(client):
    response = client.get(reverse('accounts:signup'))
    templates = response.templates
    assert 'accounts/signup.html' == templates[0].name


def test_url_for_login_page(client):
    response = client.get('/accounts/login/')
    assert response.status_code == 200


def test_url_reverse_name_for_login_page(client):
    response = client.get(reverse('accounts:login'))
    assert response.status_code == 200


def test_login_view_uses_correct_template(client):
    response = client.get(reverse('accounts:login'))
    templates = response.templates
    assert 'accounts/login.html' == templates[0].name

