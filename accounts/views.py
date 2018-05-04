from django.urls import reverse_lazy
from accounts import forms
from django.views.generic import CreateView
from accounts.models import User


# Create your views here.


class SignupPage(CreateView):
    model = User
    template_name = "accounts/signup.html"
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
