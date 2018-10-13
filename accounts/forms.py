from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from accounts.models import User, Child

help_dict = {
    "password1": '8 characters or more & not numerical only.',
    "required": "Required",
    "profile_photo":
        'Image file, size: 500x500 px, jpeg, png or gif type only.',
    'star_points': 'Required, How many points to earn a star?',
}


class UserCreateForm(UserCreationForm):
    """
    Normal users are classified as parents. They are able later on to add
    children which are also users but have mostly read-only access to the site.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].help_text = help_dict["password1"]

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_photo', 'password1',
                  'password2')
        help_texts = {
            'email': help_dict["required"],
            'profile_photo': help_dict["profile_photo"],
            'name': help_dict["required"],
        }

    def save(self, commit=False):
        user = super().save(commit=False)
        user.user_type = User.TYPE_PARENT
        # TODO Find all is_parent and is_child checks and fix them
        # TODO Fix is_superuser converted to parent in runpyton migration
        # TODO Add ssh keys to the project.
        user.save()
        return user


class ChildCreateForm(UserCreationForm):
    """
    A child user form.
    """

    star_points = forms.IntegerField(initial=15, required=True)
    star_points.help_text = help_dict['star_points']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = help_dict["password1"]
        # current_user is the user logged in classified as parent/superuser).
        self.current_user = kwargs["initial"]["current_user"]

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'star_points', 'profile_photo',
                  'password1', 'password2')
        help_texts = {
            'email': help_dict["required"],
            'profile_photo': help_dict["profile_photo"],
            'name': help_dict["required"],
        }

    def clean(self):
        """
        We need to record the star_points field value before trying to save a
        child object.

        Returns
        -------
            None
        """
        super().clean()
        self.star_points = self.cleaned_data.get("star_points")

        return self.cleaned_data

    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=False)
        user.user_type = User.TYPE_CHILD
        user.save()
        Child.objects.create(user=user, parent=self.current_user,
                             star_points=self.star_points)
        return user


class ChildUpdateForm(forms.ModelForm):
    """

    """

    class Meta:
        model = Child
        fields = ('star_points', )


class UserUpdateForm(forms.ModelForm):
    """

    """

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'profile_photo')
