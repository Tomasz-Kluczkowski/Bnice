from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].help_text = '<ul><li>Minimum 8 characters long.\n</li><li>Cannot be numerical only.\n</li><li>Cannot be similar to your personal data.\n</li><li>Common words are not allowed.</li></ul>'

    class Meta:
        model = get_user_model()

        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'email': 'Required',
        }


