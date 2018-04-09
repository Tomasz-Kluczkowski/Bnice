from django.shortcuts import render
from django.urls import reverse_lazy
from accounts import forms
from django.views.generic import CreateView, TemplateView

# Create your views here.


class SignupPage(CreateView):
    template_name = "accounts/signup.html"
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')


class LoginOk(TemplateView):
    template_name = "accounts/login_ok.html"


class LogoutOk(TemplateView):
    template_name = "accounts/logout_ok.html"
