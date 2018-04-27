from django import forms
from dashboard.models import Smiley, Oopsy

base_descriptions = [
    ('add_new_description', 'Add new description'),
    ]


class AddActionForm(forms.ModelForm):
    # This field will be hidden and only shown if user selects other in the
    # dropdown menu - then it will be set to required in jquery.
    new_description = forms.CharField(max_length=255, required=False)
    new_description.help_text = "Required, Create a new description"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].help_text = "Required"

    def clean(self):
        super().clean()
        new_description = self.cleaned_data.get("new_description")

        if new_description:
            self.cleaned_data['description'] = new_description
        return self.cleaned_data

    class Meta:
        fields = ("description", "new_description", "points")


class AddSmileyForm(AddActionForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = Smiley.objects.order_by(
                "description").values_list("description", flat=True).distinct()
        print(self.choices)
        self.fields['description'] = forms.ChoiceField(
            # empty_label="Select description",
            # queryset=Smiley.objects.order_by(
            #     "description").values_list("description", flat=True).distinct()
            choices=[(choice, choice) for choice in self.choices]
        )
        # print(list(self.fields['description'].choices))
        # self.fields['description'].choices = (
        #         [('add_new_description', 'Add new description')] +
        #         list(self.fields['description'].choices)
        # )

    class Meta(AddActionForm.Meta):
        model = Smiley
        help_texts = {"points": "Required, How much was this task worth?"}


class AddOopsyForm(AddActionForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'] = forms.ModelChoiceField(
            queryset=Oopsy.objects.distinct()
        )

    class Meta(AddActionForm.Meta):
        model = Oopsy
        help_texts = {"points": "Required, How many points to take away?"}
