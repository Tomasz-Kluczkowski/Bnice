import pytest
from accounts.models import User, Child

# from dashboard.views import DashboardPage
# from django.urls import reverse

# Mark all tests as requiring database.
pytestmark = pytest.mark.django_db


def test_dashboard_page_parent_with_no_child(client, parent_user_password):
    """Test logging to dashboard page with no children added."""
    assert User.objects.count() == 1
    username = 'tom_k'
    password = 'password'
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert len(response.context['child_list']) == 0


def test_dashboard_page_parent_with_child(client, parent_user_password,
                                          child, alt_child):
    """Test logging to dashboard page with a child added.
    Confirms only child who's parent is logged in is in the child_list."""
    username = 'tom_k'
    password = 'password'
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert Child.objects.count() == 2
    assert response.status_code == 200
    assert len(response.context['child_list']) == 1
    assert response.context['child_list'][0] == child


def test_dashboard_page_with_not_matching_user_child(client,
                                                     alt_parent_user_password,
                                                     child):
    """Tests if get_queryset restricts children in child_list by checking
    parent."""
    username = 'johny_c'
    password = 'password'
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert response.status_code == 200
    # Since child has different parent it should not be added to the queryset.
    assert len(response.context['child_list']) == 0


def test_dashboard_page_child_logged_in(client, child_user, child, alt_child):
    """Test logging to dashboard page as a child user. child_list should
    contain only the logged in child user."""
    username = 'nat_k'
    password = 'password'
    user = child_user
    user.set_password(password)
    user.save()
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert Child.objects.count() == 2
    assert response.status_code == 200
    assert len(response.context['child_list']) == 1
    assert response.context['child_list'][0] == child
