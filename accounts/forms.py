from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from accounts.models import User, Child

help_dict = {
    # "password1": '<ul><li>Minimum 8 characters long.\n</li><li>Cannot be numerical only.\n</li><li>Cannot be similar to your personal data.\n</li><li>Common words are not allowed.</li></ul>',
    "password1": '8 characters or more & not numerical only.',
    "required": "Required",
    "profile_photo": 'Image file, size: 500x500 px, jpeg, png or gif type only.'
}


class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].help_text = help_dict["password1"]

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_photo', 'password1', 'password2')
        help_texts = {
            'email': help_dict["required"],
            'profile_photo': help_dict["profile_photo"],
            'name': help_dict["required"],
        }

    def save(self, commit=False):
        user = super().save(commit=False)
        user.is_parent = True
        user.save()
        return user


class ChildCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = help_dict["password1"]
        self.current_user = kwargs["initial"]["current_user"]

    class Meta:
        model = User
        fields = ('username', 'name', 'profile_photo', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=False)
        user.is_child = True
        user.save()
        child = Child.objects.create(user=user, parent=self.current_user)
        return user
