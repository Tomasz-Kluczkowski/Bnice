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
from django.urls import path, re_path
from dashboard.views import DashboardPage, CreateChildPage, ChildDetail,\
    AddSmiley, AddOopsy

app_name = "dashboard"

urlpatterns = [
    path('', DashboardPage.as_view(), name="dashboard"),
    path('add_child/', CreateChildPage.as_view(), name="add_child"),
    re_path(
        r'^child/(?P<parent>[-\w]+)/(?P<child_username>[-\w]+)/(?P<pk>\d+)$',
        ChildDetail.as_view(), name="child_detail"),
    re_path(
        r'^child/add_smiley/(?P<parent>[-\w]+)/(?P<child_username>[-\w]+)/(?P<pk>\d+)$',
        AddSmiley.as_view(), name="add_smiley"),
    re_path(
        r'^child/add_oopsy/(?P<parent>[-\w]+)/(?P<child_username>[-\w]+)/(?P<pk>\d+)$',
        AddOopsy.as_view(), name="add_oopsy"),
]
