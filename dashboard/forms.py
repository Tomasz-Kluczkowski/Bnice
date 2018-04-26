from django import forms
from dashboard.models import Smiley, Oopsy


class AddSmileyForm(forms.ModelForm):

    class Meta:
        model = Smiley
        fields = ('description', 'points')
        help_texts = {
            'description': 'Required',
            'points': 'Required',
        }


class AddOopsyForm(forms.ModelForm):

    class Meta:
        model = Oopsy
        fields = ('description', 'points')
        help_texts = {
            'description': 'Required',
            'points': 'Required',
        }