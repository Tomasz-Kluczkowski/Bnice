import pytest
from django.urls import reverse

from accounts.models import User

pytestmark = pytest.mark.django_db


class TestLoginView:

    def test_url_for_login_page(self, client):
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200

    def test_login_view_uses_correct_template(self, client):
        response = client.get(reverse('accounts:login'))
        templates = response.templates
        assert templates[0].name == 'accounts/login.html'


class TestSignupView:

    def test_url_for_signup_page(self, client):
        response = client.get(reverse('accounts:signup'))
        assert response.status_code == 200

    def test_signup_view_uses_correct_template(self, client):
        response = client.get(reverse('accounts:signup'))
        templates = response.templates
        assert templates[0].name == 'accounts/signup.html'

    def test_signup_data_correct(self, mock_img_save, client, mock_image_file, monkeypatch):
        """Confirm new account is created."""
        monkeypatch.setattr('django.core.files.storage.FileSystemStorage.save', mock_img_save)
        form_data = {'username': 'test_username',
                     'name': 'test_name',
                     'email': 'testemail@email.com',
                     'profile_photo': mock_image_file,
                     'password1': 'passwordmustbelong',
                     'password2': 'passwordmustbelong',
                     }
        assert not User.objects.exists()
        response = client.post(reverse('accounts:signup'), form_data)
        mock_img_save.assert_called_once()
        assert response.status_code == 302
        assert response.url == reverse('accounts:login')
        assert User.objects.count() == 1
        user = User.objects.get()
        assert user.username == 'test_username'
        assert user.name == 'test_name'
        assert user.email == 'testemail@email.com'
        assert user.profile_photo == 'test.png'

    def test_signup_data_incorrect(self, client, mock_text_file):
        """Confirm new account is not created."""
        form_data = {'username': 'test_username',
                     'name': 'test_name',
                     'email': 'testemail@email.com',
                     'profile_photo': mock_text_file,
                     'password1': 'passwordmustbelong',
                     'password2': 'passwordmustbelong',
                     }
        assert not User.objects.exists()
        response = client.post(reverse('accounts:signup'), form_data)
        assert '<div class="invalid-feedback">Upload a valid image. The file you uploaded was either not an image or a ' \
               'corrupted image.</div>' in response.content.decode()
        assert not User.objects.exists()

