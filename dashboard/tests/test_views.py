import pytest
from django.urls import reverse

from Bnice import settings
from accounts.models import User, Child
from dashboard.models import Smiley, Oopsy

# Mark all tests as requiring database.
pytestmark = pytest.mark.django_db


def user_logger(client, username, password='password'):
    """Logs website users in.

    Allows easy logging of website users.

    Parameters
    ----------
    client : fixture, django-pytest fixture for website interactions
    username : str, username as in database
    password : str, password, non-hashed version

    Returns
    -------
    None
    """
    client.login(username=username, password=password)


class TestDashboardPage:

    def test_dashboard_page_parent_with_no_child(self, client, parent_user_password):
        """Test logging to dashboard page with no children added."""
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 1
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:dashboard'))
        assert response.status_code == 200
        assert len(response.context['child_list']) == 0
        templates = response.templates
        assert templates[0].name == 'dashboard/dashboard.html'

    def test_queryset_parent_with_matching_child(self, client, parent_user_password, child, alt_child):
        """Test logging to dashboard page with a child added. Confirms that only child who's parent is logged in is in
        the child_list context data."""
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:dashboard'))
        assert Child.objects.count() == 2
        assert response.status_code == 200
        assert len(response.context['child_list']) == 1
        assert response.context['child_list'][0] == child

    def test_queryset_parent_not_matching_child(self, client, alt_parent_user_password, child):
        """Tests if get_queryset restricts children in child_list by checking parent."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:dashboard'))
        assert response.status_code == 200
        # Since child has different parent it should not be added to the queryset.
        assert len(response.context['child_list']) == 0

    def test_queryset_with_child_logged_in(self, client, child_user_password, child, alt_child):
        """Test logging to dashboard page as a child user. child_list should contain only the logged in child user."""
        user_logger(client, 'nat_k')
        response = client.get('/dashboard/')
        assert Child.objects.count() == 2
        assert response.status_code == 200
        assert len(response.context['child_list']) == 1
        assert response.context['child_list'][0] == child


class TestCreateChildPage:

    def test_access_denied_to_child_users(self, client, child_user_password):
        user_logger(client, 'nat_k')
        response = client.get(reverse('dashboard:child-create'))
        assert response.status_code == 403

    def test_http_get(self, client, parent_user_password):
        user = parent_user_password
        user_logger(client, 'tom_k')
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 1
        response = client.get(reverse('dashboard:child-create'))
        assert response.status_code == 200
        # Confirm initial value for parent is passed using get_initial method.
        form = response.context['form']
        assert form.current_user == user
        templates = response.templates
        assert templates[0].name == 'dashboard/add_child.html'

    def test_http_post(self, client, parent_user_password, mock_image_file, mock_img_save, monkeypatch):
        monkeypatch.setattr('django.core.files.storage.FileSystemStorage.save', mock_img_save)
        form_data = {'username': 'kid',
                     'name': 'lili',
                     'email': 'lili@gmail.com',
                     'profile_photo': mock_image_file,
                     'star_points': 20,
                     'password1': 'new_pass',
                     'password2': 'new_pass'}
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:child-create'), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:dashboard')
        mock_img_save.assert_called_once()
        assert Child.objects.count() == 1
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 2
        child = Child.objects.get()
        child_user = User.objects.get(username='kid')
        assert child_user.username == 'kid'
        assert child_user.name == 'lili'
        assert child_user.email == 'lili@gmail.com'
        assert child_user.profile_photo == 'test.png'
        assert child.parent == parent_user_password
        assert child.star_points == 20


class TestChildDetail:

    def test_http_get_with_correct_parent(self, client, child, parent_user_password):
        """Confirm view is properly displayed for a logged in parent user who's child we want to see."""
        user_logger(client, 'tom_k')
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 2
        assert Child.objects.count() == 1
        response = client.get(reverse('dashboard:child-detail', kwargs={'pk': child.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/child_detail.html'

    def test_get_context_data_parent_user(self, client, child, parent_user_password, smiley_custom_description,
                                          oopsy_custom_description):
        """Confirm correct context data is set for the view if parent user is logged in."""
        user_logger(client, 'tom_k')
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 2
        assert Child.objects.count() == 1
        response = client.get(reverse('dashboard:child-detail', kwargs={'pk': child.pk}))
        assert response.status_code == 200
        assert len(response.context['smileys']) == 1
        assert len(response.context['oopsies']) == 1
        assert response.context['smileys'][0] == smiley_custom_description
        assert response.context['oopsies'][0] == oopsy_custom_description

    def test_get_context_data_child_user(self, client, child_user_password, child, smiley_custom_description,
                                         oopsy_custom_description):
        """Confirm correct context data is set for the view if child user is logged in."""
        user_logger(client, 'nat_k')
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 2
        assert Child.objects.count() == 1
        response = client.get(reverse('dashboard:child-detail', kwargs={'pk': child.pk}))
        assert response.status_code == 200
        assert len(response.context['smileys']) == 1
        assert len(response.context['oopsies']) == 1
        assert response.context['smileys'][0] == smiley_custom_description
        assert response.context['oopsies'][0] == oopsy_custom_description

    def test_no_edit_delete_action_for_child_user(self, client, child_user_password, smiley_custom_description,
                                                  oopsy_custom_description):
        """Confirm child user unable to add/edit/delete their actions."""
        user_logger(client, 'nat_k')
        response = client.get(reverse('dashboard:child-detail', kwargs={'pk': child_user_password.pk}))
        assert (
                   f'href="/dashboard/child/{child_user_password.pk}/smiley/{smiley_custom_description.pk}/delete/">'
               ) not in response.content.decode()

        assert (
                   f'href="/dashboard/child/{child_user_password.pk}/smiley/{smiley_custom_description.pk}/edit/">'
               ) not in response.content.decode()

        assert (
                   f'href="/dashboard/child/{child_user_password.pk}/oopsy/{oopsy_custom_description.pk}/delete/">'
               ) not in response.content.decode()

        assert (
                   f'href="/dashboard/child/{child_user_password.pk}/oopsy/{oopsy_custom_description.pk}/edit/">'
               ) not in response.content.decode()

    def test_redirects_wrong_parent_user(self, client, child, alt_parent_user_password):
        """Test view redirects when trying to access other user's child data when logged in as a parent."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:child-detail', kwargs={'pk': child.pk}))
        assert response.status_code == 403

    def test_redirects_wrong_child_user(self, client, child_user_password, alt_child):
        """Test view redirects when trying to access other child's data when logged in as a child."""
        user_logger(client, 'nat_k')
        response = client.get(reverse('dashboard:child-detail', kwargs={'pk': alt_child.pk}))
        assert response.status_code == 403


class TestAddAction:

    def test_permission_required_check(self, client, child, alt_parent_user_password):
        """Test redirection when trying to access other user's child data when logged in as a parent."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:smiley-create', kwargs={'pk': child.pk}))
        assert response.status_code == 403

    def test_http_post_smiley(self, client, child, parent_user_password):
        """Confirm Smiley object gets attributes owner and earned_on added when form is valid."""
        form_data = {'description': 'Folded washing', 'new_description': '', 'points': 5}
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:smiley-create', kwargs={'pk': child.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        assert Smiley.objects.count() == 1
        smiley = Smiley.objects.last()
        assert smiley.owner == child
        assert smiley.claimed is False
        assert smiley.points_remaining == 0
        assert smiley.description == 'Folded washing'
        assert smiley.points == 5

    def test_http_post_smiley_custom_description(self, client, child, parent_user_password):
        """Confirm Smiley object gets attributes owner and earned_on added when form is valid and new description
        overrides description field."""
        form_data = {'description': 'Add new', 'new_description': 'Testing', 'points': 5}
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:smiley-create', kwargs={'pk': child.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        assert Smiley.objects.count() == 1
        smiley = Smiley.objects.last()
        assert smiley.owner == child
        assert smiley.claimed is False
        assert smiley.points_remaining == 0
        assert smiley.description == 'Testing'
        assert smiley.points == 5

    def test_http_post_oopsy(self, client, child, parent_user_password):
        """Confirm Oopsy object gets attributes owner and earned_on added when form is valid."""
        form_data = {'description': 'Was lying', 'new_description': '', 'points': 5}
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:oopsy-create', kwargs={'pk': child.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        assert Oopsy.objects.count() == 1
        oopsy = Oopsy.objects.last()
        assert oopsy.owner == child
        assert oopsy.claimed is False
        assert oopsy.points_remaining == 0
        assert oopsy.description == 'Was lying'
        assert oopsy.points == 5

    def test_http_post_oopsy_custom_description(self, client, child, parent_user_password):
        """Confirm Oopsy object gets attributes owner and earned_on added when form is valid and new description
        overrides description field."""
        form_data = {'description': 'Add new', 'new_description': 'Testing', 'points': 5}
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:oopsy-create', kwargs={'pk': child.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        assert Oopsy.objects.count() == 1
        oopsy = Oopsy.objects.last()
        assert oopsy.owner == child
        assert oopsy.claimed is False
        assert oopsy.points_remaining == 0
        assert oopsy.description == 'Testing'
        assert oopsy.points == 5


class TestUserUpdate:

    def test_http_get(self, client, parent_user_password):
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:user-update', kwargs={'pk': parent_user_password.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/user_update.html'

    def test_permission_check(self, client, child_user_password, parent_user_password):
        """Confirm redirection when trying to update other user's profile."""
        user_logger(client, 'nat_k')
        response = client.get(reverse('dashboard:user-update', kwargs={'pk': parent_user_password.pk}))
        assert response.status_code == 403

    def test_updating_user_data(self, client, parent_user_password, mock_image_file, mock_img_save, monkeypatch):
        """Confirm user data is modified and saved in the database."""
        monkeypatch.setattr('django.core.files.storage.FileSystemStorage.save', mock_img_save)
        form_data = {
            'username': 'test_username',
            'name': 'test_name',
            'email': 'testemail@email.com',
            'profile_photo': mock_image_file
        }
        user_logger(client, 'tom_k')
        assert User.objects.exclude(username=settings.ANONYMOUS_USER_NAME).count() == 1
        response = client.post(reverse('dashboard:user-update', kwargs={'pk': parent_user_password.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:dashboard')
        mock_img_save.assert_called_once()
        user = User.objects.get(pk=parent_user_password.pk)
        assert user.username == 'test_username'
        assert user.name == 'test_name'
        assert user.email == 'testemail@email.com'
        assert user.profile_photo == 'test.png'


class TestChildUpdate:

    def test_permission_check(self, client, alt_parent_user_password, child_user, child):
        """Confirm redirection when trying to update other parent's child."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:child-update', kwargs={'pk': child.pk}))
        assert response.status_code == 403

    def test_updating_child_data(self, client, parent_user_password, child_user, child, mock_image_file, mock_img_save,
                                 monkeypatch):
        """Confirm child user data is modified and saved in the database."""
        monkeypatch.setattr('django.core.files.storage.FileSystemStorage.save', mock_img_save)
        form_data = {
            'username': 'test_username',
            'name': 'test_name',
            'email': 'testemail@email.com',
            'star_points': 12,
            'profile_photo': mock_image_file
        }
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:child-update', kwargs={'pk': child.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        mock_img_save.assert_called_once()
        child_user = User.objects.get(pk=child_user.pk)
        child = Child.objects.get(pk=child.pk)
        assert child_user.username == 'test_username'
        assert child_user.name == 'test_name'
        assert child_user.email == 'testemail@email.com'
        assert child_user.profile_photo == 'test.png'
        assert child.star_points == 12

    def test_updating_child_invalid_data(self, client, parent_user_password, child_user, child):
        """Confirm child user is requested to correct errors if invalid data in forms."""
        form_data = {'username': 'test_username!!!!',
                     'name': 'test_name',
                     'email': 'testemail@email.com',
                     'star_points': 12}
        user_logger(client, 'tom_k')
        response = client.post(reverse('dashboard:child-update', kwargs={'pk': child.pk}), form_data)
        assert response.status_code == 200
        assert (
                   'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
               ) in response.content.decode()


class TestChildDelete:

    def test_http_get_correct_parent(self, client, child, parent_user_password):
        """Confirm child delete page accessible to parent user of child to be deleted."""
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:child-delete', kwargs={'pk': child.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/child_delete.html'

    def test_http_get_incorrect_parent(self, client, child, alt_parent_user_password):
        """Confirm child delete page inaccessible to user who is not a parent of the child to be deleted."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:child-delete', kwargs={'pk': child.pk}))
        assert response.status_code == 403

    def test_http_post_deletes_child(self, client, child, parent_user_password):
        """Confirm submitting form deletes the child object from the database and redirects to dashboard view."""
        user_logger(client, 'tom_k')
        assert Child.objects.count() == 1
        response = client.post(reverse('dashboard:child-delete', kwargs={'pk': child.pk}))
        assert response.status_code == 302
        assert response.url == '/dashboard/'
        assert Child.objects.count() == 0


class TestSmileyDelete:

    def test_http_get_correct_parent(self, client, child, smiley_custom_description, parent_user_password):
        """Confirm view is accessible by parent of the child which Smiley we are deleting."""
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:smiley-delete',
                                      kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/smiley_delete.html'
        assert response.context['smiley'] == smiley_custom_description

    def test_http_get_incorrect_parent(self, client, child, smiley_custom_description, alt_parent_user_password):
        """Confirm view is not accessible by user who is not a parent of the child which Smiley we are deleting."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:smiley-delete',
                                      kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}))
        assert response.status_code == 403

    def test_http_post_deletes_smiley(self, client, child, smiley_custom_description, parent_user_password):
        """Confirm submitting form deletes the smiley object from the database and redirects to correct child detail
         view."""
        user_logger(client, 'tom_k')
        assert Smiley.objects.count() == 1
        response = client.post(reverse('dashboard:smiley-delete',
                                       kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}))
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        assert Smiley.objects.count() == 0


class TestOopsyDelete:

    def test_http_get_correct_parent(self, client, child, oopsy_custom_description, parent_user_password):
        """Confirm view is accessible by parent of the child which Oopsy we are deleting."""
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:oopsy-delete',
                                      kwargs={'child_pk': child.pk, 'pk': oopsy_custom_description.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/oopsy_delete.html'
        assert response.context['oopsy'] == oopsy_custom_description

    def test_http_get_incorrect_parent(self, client, child, oopsy_custom_description, alt_parent_user_password):
        """Confirm view is accessible by parent of the child which Oopsy we are deleting."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:oopsy-delete',
                                      kwargs={'child_pk': child.pk, 'pk': oopsy_custom_description.pk}))
        assert response.status_code == 403

    def test_http_post_deletes_oopsy(self, client, child, oopsy_custom_description, parent_user_password):
        """Confirm submitting form deletes the oopsy object from the database and redirects to correct child detail
        view."""
        user_logger(client, 'tom_k')
        assert Oopsy.objects.count() == 1
        response = client.post(reverse('dashboard:oopsy-delete',
                                       kwargs={'child_pk': child.pk, 'pk': oopsy_custom_description.pk}))
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        assert Oopsy.objects.count() == 0


class TestSmileyUpdate:

    def test_get_context_data(self, client, child, smiley_custom_description, parent_user_password):
        """Confirm correct context data is set by the view."""
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:smiley-update',
                                      kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}))
        assert response.context['child'] == child

    def test_http_get(self, client, child, smiley_custom_description, parent_user_password):
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:smiley-update',
                                      kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/smiley_update.html'

    def test_redirection_on_failed_permission_check(self, client, child, smiley_custom_description,
                                                    alt_parent_user_password):
        """Confirm redirection when trying to update smiley of child of other parent."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:smiley-update',
                                      kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}))
        assert response.status_code == 403

    def test_updating_smiley_data(self, client, child, smiley_custom_description, parent_user_password):
        """Confirm Smiley data is modified and saved in the database."""
        form_data = {'description': 'a new description', 'points': 1}
        user_logger(client, 'tom_k')
        assert Smiley.objects.count() == 1
        response = client.post(reverse('dashboard:smiley-update',
                                       kwargs={'child_pk': child.pk, 'pk': smiley_custom_description.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        smiley = Smiley.objects.last()
        assert smiley.description == 'a new description'
        assert smiley.points == 1


class TestOopsyUpdate:

    def test_get_context_data(self, client, child, oopsy_custom_description, parent_user_password):
        """Confirm correct context data is set by the view."""
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:oopsy-update',
                                      kwargs={'child_pk': child.pk, 'pk': oopsy_custom_description.pk}))
        assert response.context['child'] == child

    def test_http_get(self, client, child, oopsy_custom_description, parent_user_password):
        user_logger(client, 'tom_k')
        response = client.get(reverse('dashboard:oopsy-update', kwargs={'child_pk': child.pk,
                                                                        'pk': oopsy_custom_description.pk}))
        assert response.status_code == 200
        templates = response.templates
        assert templates[0].name == 'dashboard/oopsy_update.html'

    def test_redirection_on_failed_permission_check(self, client, child, oopsy_custom_description,
                                                    alt_parent_user_password):
        """Confirm redirection when trying to update oopsy of child of other parent."""
        user_logger(client, 'johny_c')
        response = client.get(reverse('dashboard:oopsy-update',
                                      kwargs={'child_pk': child.pk, 'pk': oopsy_custom_description.pk}))
        assert response.status_code == 403

    def test_updating_oopsy_data(self, client, child, oopsy_custom_description, parent_user_password):
        """Confirm Oopsy data is modified and saved in the database."""
        form_data = {'description': 'a new description', 'points': 1}
        user_logger(client, 'tom_k')
        assert Oopsy.objects.count() == 1
        response = client.post(reverse('dashboard:oopsy-update',
                                       kwargs={'child_pk': child.pk, 'pk': oopsy_custom_description.pk}), form_data)
        assert response.status_code == 302
        assert response.url == reverse('dashboard:child-detail', kwargs={'pk': child.pk})
        oopsy = Oopsy.objects.last()
        assert oopsy.description == 'a new description'
        assert oopsy.points == 1
