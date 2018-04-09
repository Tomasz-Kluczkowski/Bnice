"""Bnice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import SignupPage, LoginOk, LogoutOk
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('signup/', SignupPage.as_view(), name="signup"),
    path('login/',
         auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('login_ok/', LoginOk.as_view(), name="login_ok"),
    path('logout_ok/', LogoutOk.as_view(), name="logout_ok"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
