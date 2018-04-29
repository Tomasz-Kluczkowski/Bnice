from django import forms
from dashboard.models import Smiley, Oopsy

base_smileys = [
    'Add new',
    'Folded washing',
    'Cleaned bathroom',
    'Mopped floor',
]

base_oopsies = [
    'Add new',
    "Was lying",
    'Left mess',
    'Talked back to parent',
]


class AddActionForm(forms.ModelForm):
    # This field will be hidden and only shown if user selects 'Add new' in the
    # dropdown menu - then it will be set to required in jquery.
    new_description = forms.CharField(max_length=255, required=False)
    new_description.help_text = "Required, Create a new description"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].help_text = "Required"

    def clean(self):
        super().clean()
        # If user has given a new description for the action it will overwrite
        # whatever was selected in the dropdown menu.
        new_description = self.cleaned_data.get("new_description")

        if new_description:
            self.cleaned_data['description'] = new_description
        return self.cleaned_data

    def set_description(self, model, initial_choice_list):
        """Set 'description' field to forms.Choicefield.

        Create a list of distinct descriptions for actions using appropriate
        to the model base list and add that to options in select html element
        when rendered in the form.

        Parameters
        ----------
        model : Action
            Subclass of Action model (Smiley or Oopsy).
        initial_choice_list : list(str)
            List of strings describing action to show in the dropdown menu.

        Returns
        -------
            None
        """
        print(model)
        choices = list(model.objects.order_by(
            "description").values_list("description", flat=True).distinct())
        distinct_choices = initial_choice_list + [
            choice for choice in choices if choice not in initial_choice_list]
        self.fields['description'] = forms.ChoiceField(
            choices=[(choice, choice) for choice in distinct_choices]
        )

    class Meta:
        fields = ("description", "new_description", "points")


class AddSmileyForm(AddActionForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_description(Smiley, base_smileys)

    class Meta(AddActionForm.Meta):
        model = Smiley
        help_texts = {"points": "Required, How much was this task worth?"}


class AddOopsyForm(AddActionForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_description(Oopsy, base_oopsies)

    class Meta(AddActionForm.Meta):
        model = Oopsy
        help_texts = {"points": "Required, How many points to take away?"}
