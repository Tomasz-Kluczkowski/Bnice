import pytest
from accounts.models import User

from dashboard.views import DashboardPage
from django.urls import reverse

# Mark all tests as requiring database.
pytestmark = pytest.mark.django_db


def test_dashboard_page_parent_with_no_children(client, parent_user_password):
    """Test logging to dashboard page with no children added."""
    assert User.objects.count() == 1
    username = 'tom_k'
    password = 'password'
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert len(response.context['child_list']) == 0


def test_dashboard_page_with_parent_with_children(client, parent_user_password,
                                                  child):
    """Test logging to dashboard page with a child added."""
    username = 'tom_k'
    password = 'password'
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert len(response.context['child_list']) == 1
    assert response.context['child_list'][0] == child
