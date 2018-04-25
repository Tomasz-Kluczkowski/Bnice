from django import forms
from dashboard.models import Smiley, Oopsy


class AddSmileyForm(forms.ModelForm):

    class Meta:
        model = Smiley
        fields = ('description', )
        help_texts = {
            'description': 'Required',
        }


class AddOopsyForm(forms.ModelForm):

    class Meta:
        model = Oopsy
        fields = ('description', )
        help_texts = {
            'description': 'Required',
        }