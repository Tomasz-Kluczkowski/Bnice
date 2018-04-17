from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from accounts.models import User, Child


class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].help_text = '<ul><li>Minimum 8 characters long.\n</li><li>Cannot be numerical only.\n</li><li>Cannot be similar to your personal data.\n</li><li>Common words are not allowed.</li></ul>'

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_pic', 'password1', 'password2')
        help_texts = {
            'email': 'Required',
            'profile_pic': 'Image file, size 500x500 px. Jpeg, png or gif type only.'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_parent = True
        if commit:
            user.save()
        return user


class ChildCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = '<ul><li>Minimum 8 characters long.\n</li><li>Cannot be numerical only.\n</li><li>Cannot be similar to your personal data.\n</li><li>Common words are not allowed.</li></ul>'
        self.current_user = kwargs["initial"]["current_user"]

    class Meta:
        model = User
        fields = ('username', 'profile_pic', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_child = True
        user.save()
        child = Child.objects.create(user=user, parent=self.current_user)
        return user
