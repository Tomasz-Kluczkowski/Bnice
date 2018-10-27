import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_redirect_to_login(client):
    response = client.get(reverse('dashboard:dashboard'))
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/dashboard/'
