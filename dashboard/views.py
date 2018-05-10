from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from accounts.models import Child, User
from accounts.forms import ChildCreateForm
from dashboard.models import Smiley, Oopsy
from dashboard.forms import AddSmileyForm, AddOopsyForm
from dashboard.services import StarAwarding


# Create your views here.


class DashboardPage(LoginRequiredMixin, ListView):
    model = Child
    template_name = "dashboard/dashboard.html"

    def get_queryset(self):
        if self.request.user.is_child:
            return Child.objects.filter(pk=self.request.user.pk)
        else:
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


class ChildDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Awards stars before displaying Child details.

    """
    model = Child
    template_name = "dashboard/child_detail.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        child = self.get_object()
        current_user = self.request.user
        if current_user.is_authenticated and current_user.is_child:
            kwargs['parent'] = Child.objects.get(
                user=current_user).parent.username
        kwargs['smileys'] = Smiley.objects.filter(
            owner=child).order_by("earned_on")
        kwargs['oopsies'] = Oopsy.objects.filter(
            owner=child).order_by("earned_on")
        star_awarding = StarAwarding(kwargs['smileys'], kwargs['oopsies'],
                                     child.star_points)
        star_awarding.award_star()
        return super().get_context_data(**kwargs)

    def test_func(self):
        """Allow access only to logged in users.

        We have to check differently for parent and child users hence if/elif.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        parent = self.kwargs["parent"]
        if current_user.is_parent and current_user.username == parent:
            return True
        elif current_user.is_child and current_user.pk == int(self.kwargs["pk"]):
            return True
        else:
            return False


class AddAction(LoginRequiredMixin, UserPassesTestMixin, CreateView):

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


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'email', 'profile_photo')
    template_name = 'dashboard/user_update.html'
    success_url = reverse_lazy('dashboard:dashboard')


class ChildUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'name', 'email', 'profile_photo')
    template_name = 'dashboard/user_update.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        kwargs['parent'] = Child.objects.get(
            user__pk=self.object.pk).parent.username
        return super().get_context_data(**kwargs)


class ChildDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Child
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'dashboard/child_delete.html'

    def test_func(self):
        """Allow access only to logged in users.

        We have to check differently for parent and child users hence if/elif.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        child = self.get_object()
        parent = Child.objects.get(
            user__pk=child.pk).parent.username
        if current_user.is_parent and current_user.username == parent:
            return True
        else:
            return False
