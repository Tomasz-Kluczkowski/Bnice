from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from accounts.models import Child
from accounts.forms import ChildCreateForm
from dashboard.models import Smiley, Oopsy
from dashboard.forms import AddSmileyForm, AddOopsyForm
from dashboard.services import get_total_points

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
    """
    Here we need logic that will allow claiming stars for points gathered by
    a child. This logic has to be run when child detail is updated.
    """
    model = Child
    template_name = "dashboard/child_detail.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        kwargs['smileys'] = Smiley.objects.filter(
            owner=self.object).order_by("-earned_on")
        kwargs['oopsies'] = Oopsy.objects.filter(
            owner=self.object).order_by("-earned_on")
        print(get_total_points(kwargs['smileys'], kwargs['oopsies']))
        return super().get_context_data(**kwargs)

    def test_func(self):
        current_user = self.request.user.username
        parent = self.kwargs["parent"]
        if current_user == parent:
            return True
        else:
            return False


class AddAction(UserPassesTestMixin, LoginRequiredMixin, CreateView):

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


class AddSmiley(AddAction):
    model = Smiley
    template_name = "dashboard/add_action.html"
    form_class = AddSmileyForm


class AddOopsy(AddAction):
    model = Oopsy
    template_name = "dashboard/add_action.html"
    form_class = AddOopsyForm

