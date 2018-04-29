from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from accounts.models import Child
from dashboard.models import Smiley, Oopsy
from accounts.forms import ChildCreateForm
from dashboard.forms import AddSmileyForm, AddOopsyForm
from django.core.exceptions import PermissionDenied
from django.utils import timezone

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

    # def get_context_data(self, **kwargs):
    #     kwargs['child_list'] = Child.objects.filter(parent=self.request.user)
    #     return super().get_context_data(**kwargs)

    def get_initial(self):
        self.initial.update({"current_user": self.request.user})
        return self.initial


class ChildDetail(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Child
    template_name = "dashboard/child_detail.html"

    def get_context_data(self, **kwargs):
        kwargs['smileys'] = Smiley.objects.filter(
            owner=self.object).order_by("-earned_on")
        kwargs['oopsies'] = Oopsy.objects.filter(
            owner=self.object).order_by("-earned_on")
        return super().get_context_data(**kwargs)

    def test_func(self):
        current_user = self.request.user.username
        parent = self.kwargs["parent"]
        if current_user == parent:
            return True
        else:
            return False


class AddSmiley(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Smiley
    template_name = "dashboard/add_action.html"
    form_class = AddSmileyForm

    def get_context_data(self, **kwargs):
        kwargs['child'] = Child.objects.get(pk=self.kwargs["pk"])
        return super().get_context_data(**kwargs)

    def test_func(self):
        current_user = self.request.user.username
        parent = self.kwargs["parent"]
        if current_user == parent:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.owner = Child.objects.get(pk=self.kwargs["pk"])
        form.instance.earned_on = timezone.now()
        form.save()
        return super().form_valid(form)


class AddOopsy(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Oopsy
    template_name = "dashboard/add_action.html"
    form_class = AddOopsyForm

    def get_context_data(self, **kwargs):
        kwargs['child'] = Child.objects.get(pk=self.kwargs["pk"])
        return super().get_context_data(**kwargs)

    def test_func(self):
        current_user = self.request.user.username
        parent = self.kwargs["parent"]
        if current_user == parent:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.owner = Child.objects.get(pk=self.kwargs["pk"])
        form.instance.earned_on = timezone.now()
        form.save()
        return super().form_valid(form)
