import pytest
from accounts.models import User, Child
from dashboard.models import Smiley, Oopsy

# from dashboard.views import DashboardPage
# from django.urls import reverse

# Mark all tests as requiring database.
pytestmark = pytest.mark.django_db


def user_logger(client, username, password='password'):
    client.login(username=username, password=password)


# Tests of DashBoardPage view.


def test_dashboard_page_parent_with_no_child(client, parent_user_password):
    """Test logging to dashboard page with no children added."""
    assert User.objects.count() == 1
    user_logger(client, 'tom_k')
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert len(response.context['child_list']) == 0
    templates = response.templates
    assert templates[0].name == 'dashboard/dashboard.html'


def test_dashboard_page_parent_with_child(client, parent_user_password,
                                          child, alt_child):
    """Test logging to dashboard page with a child added.
    Confirms only child who's parent is logged in is in the child_list."""
    user_logger(client, 'tom_k')
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
    user_logger(client, 'johny_c')
    response = client.get('/dashboard/')
    assert response.status_code == 200
    # Since child has different parent it should not be added to the queryset.
    assert len(response.context['child_list']) == 0


def test_dashboard_page_child_logged_in(client, child_user, child, alt_child):
    """Test logging to dashboard page as a child user. child_list should
    contain only the logged in child user."""
    password = 'password'
    user = child_user
    user.set_password(password)
    user.save()
    user_logger(client, 'nat_k')
    response = client.get('/dashboard/')
    assert Child.objects.count() == 2
    assert response.status_code == 200
    assert len(response.context['child_list']) == 1
    assert response.context['child_list'][0] == child


# Tests of CreateChildPage view.

def test_create_child_page_view(client, parent_user):
    password = 'password'
    user = parent_user
    user.set_password(password)
    user.save()
    user_logger(client, 'tom_k')
    assert User.objects.count() == 1
    response = client.get('/dashboard/add/child/')
    assert response.status_code == 200
    # Comfirm initial value for parent is passed using get_initial method.
    form = response.context['form']
    assert form.current_user == user
    templates = response.templates
    assert templates[0].name == 'dashboard/add_child.html'

    # Tests of ChildDetail view.
    """Confirm children of the parent user logged in get passed as context
    data."""


def test_child_detail_view(client, child, parent_user_password):
    """Confirm view is properly displayed for a logged in parent user who's
    child we want to see."""
    user_logger(client, 'tom_k')
    assert User.objects.count() == 2
    assert Child.objects.count() == 1
    response = client.get('/dashboard/child/detail/tom_k/nat_k/1')
    assert response.status_code == 200
    templates = response.templates
    assert templates[0].name == 'dashboard/child_detail.html'


def test_child_detail_view_context_data(client, child, parent_user_password,
                                        smiley_custom_description,
                                        oopsy_custom_description):
    """Confirm correct context data is set for the view if parent user is
    logged in."""
    user_logger(client, 'tom_k')
    assert User.objects.count() == 2
    assert Child.objects.count() == 1
    response = client.get('/dashboard/child/detail/tom_k/nat_k/1')
    assert response.status_code == 200
    assert len(response.context['smileys']) == 1
    assert len(response.context['oopsies']) == 1
    assert response.context['smileys'][0] == smiley_custom_description
    assert response.context['oopsies'][0] == oopsy_custom_description


def test_child_detail_view_child_logged_in(client, child_user_password,
                                           smiley_custom_description,
                                           oopsy_custom_description):
    """Confirm correct context data is set for the view if child user is
    logged in."""
    user_logger(client, 'nat_k')
    assert User.objects.count() == 2
    assert Child.objects.count() == 1
    response = client.get('/dashboard/child/detail/tom_k/nat_k/1')
    assert response.status_code == 200
    assert response.context['parent'] == 'tom_k'
    assert len(response.context['smileys']) == 1
    assert len(response.context['oopsies']) == 1
    assert response.context['smileys'][0] == smiley_custom_description
    assert response.context['oopsies'][0] == oopsy_custom_description


def test_child_detail_view_test_func_parent(client, child,
                                            parent_user_password):
    """Test test_func when trying to access other user's child data when logged
    in as a parent."""
    user_logger(client, 'tom_k')
    response = client.get('/dashboard/child/detail/jeffrey/gonzo/1')
    assert response.status_code == 302


def test_child_detail_view_test_func_child(client, child,
                                           child_user_password):
    """Test test_func when trying to access other child's data when logged in
    as a child."""
    user_logger(client, 'nat_k')
    response = client.get('/dashboard/child/detail/jeffrey/gonzo/2')
    assert response.status_code == 302


# Tests of AddAction view.

def test_add_action_view_context(client, child, alt_child,
                                 parent_user_password):
    """Confirm only children of the parent user logged in get passed as context
    data. (alt_child should be filtered out)."""
    user_logger(client, 'tom_k')
    response = client.get('/dashboard/child/add_smiley/tom_k/nat_k/1')
    assert response.status_code == 200
    assert Child.objects.count() == 2
    assert response.context['child'] == child


def test_add_action_test_func(client, parent_user_password):
    """Test test_func when trying to access other user's child data when logged
    in as a parent."""
    user_logger(client, 'tom_k')
    response = client.get('/dashboard/child/add_smiley/jeffrey/nat_k/1')
    assert response.status_code == 302


def test_form_valid_smiley(client, child, parent_user):
    """Confirm Smiley object gets attributes owner and earned_on added
    when form is valid."""
    password = 'password'
    form_data = {'description': 'Folded washing',
                 'new_description': '',
                 'points': 5}
    user = parent_user
    user.set_password(password)
    user.save()
    user_logger(client, 'tom_k')
    response = client.post('/dashboard/child/add_smiley/tom_k/nat_k/1',
                           form_data)

    assert response.status_code == 302
    assert response.url == '/dashboard/child/detail/tom_k/nat_k/1'
    assert Smiley.objects.count() == 1
    smiley = Smiley.objects.last()
    assert smiley.owner == child
    assert smiley.claimed is False
    assert smiley.points_remaining == 0
    assert smiley.description == 'Folded washing'
    assert smiley.points == 5


def test_form_valid_smiley_custom_description(client, child, parent_user):
    """Confirm Smiley object gets attributes owner and earned_on added
    when form is valid."""
    password = 'password'
    form_data = {'description': 'Add new',
                 'new_description': 'Testing',
                 'points': 5}
    user = parent_user
    user.set_password(password)
    user.save()
    user_logger(client, 'tom_k')
    response = client.post('/dashboard/child/add_smiley/tom_k/nat_k/1',
                           form_data)

    assert response.status_code == 302
    assert response.url == '/dashboard/child/detail/tom_k/nat_k/1'
    assert Smiley.objects.count() == 1
    smiley = Smiley.objects.last()
    assert smiley.owner == child
    assert smiley.claimed is False
    assert smiley.points_remaining == 0
    assert smiley.description == 'Testing'
    assert smiley.points == 5


def test_form_valid_oopsy(client, child, parent_user):
    """Confirm Oopsy object gets attributes owner and earned_on added
    when form is valid."""
    password = 'password'
    form_data = {'description': 'Was lying',
                 'new_description': '',
                 'points': 5}
    user = parent_user
    user.set_password(password)
    user.save()
    user_logger(client, 'tom_k')
    response = client.post('/dashboard/child/add_oopsy/tom_k/nat_k/1',
                           form_data)

    assert response.status_code == 302
    assert response.url == '/dashboard/child/detail/tom_k/nat_k/1'
    assert Oopsy.objects.count() == 1
    oopsy = Oopsy.objects.last()
    assert oopsy.owner == child
    assert oopsy.claimed is False
    assert oopsy.points_remaining == 0
    assert oopsy.description == 'Was lying'
    assert oopsy.points == 5


def test_form_valid_oopsy_custom_description(client, child, parent_user):
    """Confirm Oopsy object gets attributes owner and earned_on added
    when form is valid."""
    password = 'password'
    form_data = {'description': 'Add new',
                 'new_description': 'Testing',
                 'points': 5}
    user = parent_user
    user.set_password(password)
    user.save()
    user_logger(client, 'tom_k')
    response = client.post('/dashboard/child/add_oopsy/tom_k/nat_k/1',
                           form_data)

    assert response.status_code == 302
    assert response.url == '/dashboard/child/detail/tom_k/nat_k/1'
    assert Oopsy.objects.count() == 1
    oopsy = Oopsy.objects.last()
    assert oopsy.owner == child
    assert oopsy.claimed is False
    assert oopsy.points_remaining == 0
    assert oopsy.description == 'Testing'
    assert oopsy.points == 5


# Tests for UserUpdate view.

def test_get_request(client, parent_user_password):
    user_logger(client, 'tom_k')
    response = client.get('/dashboard/user/update/1')
    assert response.status_code == 200
    templates = response.templates
    assert templates[0].name == 'dashboard/user_update.html'


def test_test_func_redirects(client, child_user_password, parent_user_password):
    """Confirm test_func redirects to login when updating other user's
    profile."""
    user_logger(client, 'nat_k')
    response = client.get('/dashboard/user/update/2')
    assert response.status_code == 302
    assert response.url == '/accounts/login/?next=/dashboard/user/update/2'


def test_updating_user_data(client, parent_user):
    password = 'password'
    form_data = {'username': 'test_username',
                 'email': 'testemail@email.com'}
    user = parent_user
    user.set_password(password)
    user.save()
    user_logger(client, 'tom_k')
    assert User.objects.count() == 1
    response = client.post('/dashboard/user/update/1', form_data)
    assert response.status_code == 302
    assert response.url == '/dashboard/'
    user.refresh_from_db()
    assert user.username == 'test_username'
    assert user.email == 'testemail@email.com'

# Tests for ChildUpdate view.


def test_get_context_data(client, child, child_user_password):
    user_logger(client, 'nat_k')
    response = client.get('/dashboard/child/update/1')
    assert response.context['parent'] == 'tom_k'
    assert response.status_code == 200
    templates = response.templates
    assert templates[0].name == 'dashboard/user_update.html'


def test_updating_child_data(client, child_user):
    password = 'password'
    form_data = {'username': 'test_username',
                 'name': 'test_name',
                 'email': 'testemail@email.com'}
    user = child_user
    user.set_password(password)
    user.save()
    user_logger(client, 'nat_k')
    assert User.objects.count() == 1
    response = client.post('/dashboard/child/update/1', form_data)
    assert response.status_code == 302
    assert response.url == '/dashboard/'
    user.refresh_from_db()
    assert user.username == 'test_username'
    assert user.name == 'test_name'
    assert user.email == 'testemail@email.com'


# Test ChildDelete view.

