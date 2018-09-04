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
from django.urls import path
from dashboard.views import (
    DashboardPage, CreateChildPage, ChildDetail,
    AddSmiley, AddOopsy, UserUpdate, ChildUpdate, ChildDelete,
    SmileyDelete, OopsyDelete, SmileyUpdate, OopsyUpdate)

app_name = "dashboard"

urlpatterns = [
    path('', DashboardPage.as_view(), name="dashboard"),
    path('child/<int:pk>/',
         ChildDetail.as_view(), name="child-detail"),
    path('child/new/', CreateChildPage.as_view(), name="child-create"),
    path('child/<int:pk>/edit/', ChildUpdate.as_view(),
         name="child-update"),
    path('child/<int:pk>/delete/', ChildDelete.as_view(), name='child-delete'),
    path('child/<int:pk>/smiley/new/', AddSmiley.as_view(),
         name="smiley-create"),
    path('child/<int:child_pk>/smiley/<int:pk>/delete/',
         SmileyDelete.as_view(),
         name='smiley-delete'),
    path('child/<int:child_pk>/smiley/<int:pk>/edit/', SmileyUpdate.as_view(),
         name='smiley-update'),
    path('child/<int:pk>/oopsy/new/', AddOopsy.as_view(), name="oopsy-create"),
    path('child/<int:child_pk>/oopsy/<int:pk>/delete/', OopsyDelete.as_view(),
         name='oopsy-delete'),
    path('child/<int:child_pk>/oopsy/<int:pk>/edit/', OopsyUpdate.as_view(),
         name='oopsy-update'),
    path('user/update/<int:pk>/', UserUpdate.as_view(),
         name="user_update"),
]
