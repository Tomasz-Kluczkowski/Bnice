from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.http import HttpResponseRedirect

from accounts.models import Child, User
from accounts.forms import ChildCreateForm, ChildUpdateForm, UserUpdateForm
from core.mixins.permission_mixins import PermissionRequiredMixin403
from dashboard.models import Smiley, Oopsy
from dashboard.forms import AddSmileyForm, AddOopsyForm
from dashboard.services import StarAwarding


class DashboardPage(ListView):
    model = Child
    template_name = "dashboard/dashboard.html"

    def get_queryset(self):
        if self.request.user.is_child():
            return Child.objects.filter(pk=self.request.user.pk).select_related('parent', 'user')
        else:
            return Child.objects.filter(parent=self.request.user).select_related('parent', 'user')


class CreateChildPage(CreateView):
    model = Child
    template_name = "dashboard/add_child.html"
    form_class = ChildCreateForm
    success_url = reverse_lazy('dashboard:dashboard')

    def get_initial(self):
        self.initial.update({"current_user": self.request.user})
        return self.initial


class ChildDetail(PermissionRequiredMixin403, DetailView):
    """Awards stars before displaying Child details."""
    model = Child
    template_name = "dashboard/child_detail.html"
    permission_required = 'accounts.view_child_instance'

    def get_context_data(self, **kwargs):
        child = self.get_object()
        kwargs['smileys'] = child.smileys.all()
        kwargs['oopsies'] = child.oopsies.all()
        star_awarding = StarAwarding(kwargs['smileys'], kwargs['oopsies'], child.star_points)
        star_awarding.award_star()
        return super().get_context_data(**kwargs)


class AddAction(PermissionRequiredMixin403, CreateView):
    permission_required = 'accounts.edit_child_instance'

    def dispatch(self, request, *args, **kwargs):
        self.child = get_object_or_404(Child.objects, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_permission_object(self):
        return self.child

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.owner = self.child
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


class UserUpdate(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'dashboard/user_update.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def test_func(self):
        """Allow access only to logged in user who's data we are trying to change.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        user_pk = self.kwargs['pk']
        user = User.objects.get(pk=user_pk)
        if current_user == user:
            return True
        else:
            return False


class ChildUpdate(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    child_form_class = ChildUpdateForm
    template_name = 'dashboard/child_update.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('dashboard:child-detail', **kwargs)

    def get_context_data(self, **kwargs):
        child = Child.objects.get(user__pk=self.object.pk)
        kwargs['parent'] = child.parent.username
        kwargs['child_form'] = self.child_form_class(initial={'star_points': child.star_points})
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        child = Child.objects.get(user__pk=self.object.pk)
        user_form = self.form_class(request.POST, request.FILES, instance=self.object)
        child_form = self.child_form_class(request.POST, instance=child)
        if user_form.is_valid() and child_form.is_valid():
            user_data = user_form.save(commit=False)
            user_data.save()
            child_data = child_form.save(commit=False)
            child_data.save()
            return HttpResponseRedirect(self.get_success_url(kwargs={'pk': child.user.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=user_form, child_form=child_form))

    def test_func(self):
        """Allow access only to logged in parent users who match child to be
        updated parent.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        child_user = self.get_object()
        child = Child.objects.get(user=child_user)
        parent = child.parent.username
        if current_user.is_parent() and current_user.username == parent:
            return True
        else:
            return False


class ChildDelete(UserPassesTestMixin, DeleteView):
    model = Child
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'dashboard/child_delete.html'

    def test_func(self):
        """Allow access only to logged in parent users who match child's to be deleted parent.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        child = self.get_object()
        parent = child.parent.username
        if current_user.is_parent() and current_user.username == parent:
            return True
        else:
            return False


class ActionDeleteBase(UserPassesTestMixin, DeleteView):
    """Base class for deleting actions. Not to be used on its own."""

    model = None

    def get_queryset(self):
        qs = self.model.objects.filter(
            pk=self.kwargs.get('pk')).select_related('owner', 'owner__user', 'owner__parent')
        return qs

    def get_context_data(self, **kwargs):
        action = self.object
        kwargs['child'] = action.owner
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        action = self.object
        child = action.owner
        return reverse('dashboard:child-detail', kwargs={'pk': child.pk})

    def test_func(self):
        """Allow access only to logged in parent user who is parent of the child who's action we are deleting.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        action = self.get_object()
        parent = action.owner.parent.username
        if current_user.is_parent() and current_user.username == parent:
            return True
        else:
            return False


class SmileyDelete(ActionDeleteBase):
    """Delete smiley actions."""

    model = Smiley
    template_name = 'dashboard/smiley_delete.html'


class OopsyDelete(ActionDeleteBase):
    """Delete oopsy actions."""

    model = Oopsy
    template_name = 'dashboard/oopsy_delete.html'


class ActionUpdateBase(UserPassesTestMixin, UpdateView):
    """Base class for updating unclaimed smiley and oopsy objects. Do not use on its own."""

    model = None
    fields = ('description', 'points')

    def get_context_data(self, **kwargs):
        action = self.object
        kwargs['child'] = action.owner
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        action = self.object
        child = action.owner
        return reverse('dashboard:child-detail', kwargs={'pk': child.pk})

    def test_func(self):
        """Allow access only to logged in parent user who is parent of the child who's action we are updating.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        action = self.get_object()
        parent = action.owner.parent.username
        if current_user.is_parent() and current_user.username == parent:
            return True
        else:
            return False


class SmileyUpdate(ActionUpdateBase):
    model = Smiley
    template_name = 'dashboard/smiley_update.html'


class OopsyUpdate(ActionUpdateBase):
    model = Oopsy
    template_name = 'dashboard/oopsy_update.html'
