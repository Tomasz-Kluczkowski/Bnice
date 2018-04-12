from django.urls import reverse_lazy
from accounts import forms
from django.views.generic import CreateView

# Create your views here.


class SignupPage(CreateView):
    template_name = "accounts/signup.html"
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')

