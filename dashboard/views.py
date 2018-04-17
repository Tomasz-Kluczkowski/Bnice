from django.views.generic import ListView, TemplateView, CreateView
from django.urls import reverse_lazy
from accounts.models import Child
from accounts.forms import ChildCreateForm

# Create your views here.


class DashboardPage(TemplateView):
    template_name = "dashboard/dashboard.html"


class CreateChildPage(CreateView):
    model = Child
    template_name = "dashboard/add_child.html"
    form_class = ChildCreateForm
    success_url = reverse_lazy('dashboard:dashboard')

    def get_initial(self):
        self.initial.update({"current_user": self.request.user})
        return self.initial
