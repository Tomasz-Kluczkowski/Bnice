from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.


class DashboardPage(TemplateView):
    template_name = "dashboard/dashboard.html"
