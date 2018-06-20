import pytest
from accounts.models import User, Child

# from dashboard.views import DashboardPage
# from django.urls import reverse

# Mark all tests as requiring database.
pytestmark = pytest.mark.django_db

# Tests of DashBoardPage view.


def test_dashboard_page_parent_with_no_child(client, parent_user_password):
    """Test logging to dashboard page with no children added."""
    assert User.objects.count() == 1
    username = 'tom_k'
    password = 'password'
    client.login(username=username, password=password)
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert len(response.context['child_list']) == 0
    templates = response.templates
    assert templates[0].name == 'dashboard/dashboard.html'


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


# Tests of CreateChildPage view.

def test_create_child_page_view(client, parent_user):
    username = 'tom_k'
    password = 'password'
    user = parent_user
    user.set_password(password)
    user.save()
    assert User.objects.count() == 1
    client.login(username=username, password=password)
    response = client.get('/dashboard/add/child/')
    assert response.status_code == 200
    # Comfirm initial value for parent is passed using get_initial method.
    form = response.context['form']
    assert form.current_user == user
    templates = response.templates
    assert templates[0].name == 'dashboard/add_child.html'


# Tests of ChildDetail view.

def test_child_detail_view(client, child, parent_user_password):
    username = 'tom_k'
    password = 'password'
    assert User.objects.count() == 2
    assert Child.objects.count() == 1
    client.login(username=username, password=password)
    response = client.get('/dashboard/child/detail/tom_k/nat_k/1')
    assert response.status_code == 200
    templates = response.templates
    assert templates[0].name == 'dashboard/child_detail.html'

