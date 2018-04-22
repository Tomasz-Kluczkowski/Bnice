from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from accounts.models import Child
from accounts.forms import ChildCreateForm
from django.core.exceptions import PermissionDenied

# Create your views here.


class DashboardPage(LoginRequiredMixin, ListView):
    model = Child
    template_name = "dashboard/dashboard.html"

    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)


class CreateChildPage(LoginRequiredMixin, CreateView):
    model = Child
    template_name = "dashboard/add_child.html"
    form_class = ChildCreateForm
    success_url = reverse_lazy('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        kwargs['child_list'] = Child.objects.filter(parent=self.request.user)
        return super().get_context_data(**kwargs)

    def get_initial(self):
        self.initial.update({"current_user": self.request.user})
        return self.initial


class ChildDetail(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Child
    template_name = "dashboard/child_detail.html"

    def test_func(self):
        current_user = self.request.user.username
        parent = self.kwargs["parent"]
        if current_user == parent:
            return True
        else:
            raise PermissionDenied
