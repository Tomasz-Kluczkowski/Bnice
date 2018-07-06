from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from accounts.models import Child, User
from accounts.forms import ChildCreateForm, ChildUpdateForm
from dashboard.models import Smiley, Oopsy
from dashboard.forms import AddSmileyForm, AddOopsyForm
from dashboard.services import StarAwarding


# Create your views here.


class DashboardPage(LoginRequiredMixin, ListView):
    model = Child
    template_name = "dashboard/dashboard.html"

    def get_queryset(self):
        if self.request.user.is_child:
            return Child.objects.filter(
                pk=self.request.user.pk).select_related('parent', 'user')
        else:
            return Child.objects.filter(
                parent=self.request.user).select_related('parent', 'user')


class CreateChildPage(LoginRequiredMixin, CreateView):
    model = Child
    template_name = "dashboard/add_child.html"
    form_class = ChildCreateForm
    success_url = reverse_lazy('dashboard:dashboard')

    def get_initial(self):
        self.initial.update({"current_user": self.request.user})
        return self.initial


class ChildDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Awards stars before displaying Child details.

    """
    model = Child
    template_name = "dashboard/child_detail.html"

    def get_context_data(self, **kwargs):
        child = self.get_object()
        current_user = self.request.user
        if current_user.is_child:
            kwargs['parent'] = child.parent.username
        kwargs['smileys'] = child.smiley_set.all()
        kwargs['oopsies'] = child.oopsy_set.all()
        star_awarding = StarAwarding(kwargs['smileys'], kwargs['oopsies'],
                                     child.star_points)
        star_awarding.award_star()
        return super().get_context_data(**kwargs)

    def test_func(self):
        """Allow access only to parent / child users.

        We have to check differently for parent and child users hence if/elif.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        parent = self.kwargs["parent"]
        if current_user.is_parent and current_user.username == parent:
            return True
        elif current_user.is_child and current_user.pk == int(
                self.kwargs["pk"]):
            return True
        else:
            return False


class AddAction(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    def get_context_data(self, **kwargs):
        kwargs['child'] = Child.objects.get(pk=self.kwargs["pk"])
        return super().get_context_data(**kwargs)

    def test_func(self):
        current_user = self.request.user
        parent = self.kwargs["parent"]
        if current_user.is_parent and current_user.username == parent:
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


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ('username', 'email', 'profile_photo')
    template_name = 'dashboard/user_update.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def test_func(self):
        """Allow access only to logged in user who's data we are trying
        to change.

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


class ChildUpdate(LoginRequiredMixin, UpdateView):
    model = User
    child_form_class = ChildUpdateForm
    fields = ('username', 'name', 'email', 'profile_photo',)
    template_name = 'dashboard/child_update.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        child = Child.objects.get(user__pk=self.object.pk)
        kwargs['parent'] = child.parent.username
        kwargs['child_form'] = self.child_form_class(
            initial={'star_points': child.star_points})
        return super().get_context_data(**kwargs)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.form_class(request.POST)
    #     form2 = self.second_form_class(request.POST)
    #
    #     if form.is_valid() and form2.is_valid():
    #         userdata = form.save(commit=False)
    #         # used to set the password, but no longer necesarry
    #         userdata.save()
    #         employeedata = form2.save(commit=False)
    #         employeedata.user = userdata
    #         employeedata.save()
    #         messages.success(self.request, 'Settings saved successfully')
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         return self.render_to_response(
    #             self.get_context_data(form=form, form2=form2))


class ChildDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Child
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'dashboard/child_delete.html'

    def test_func(self):
        """Allow access only to logged in parent users who match child's to be
        deleted parent.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        child = self.get_object()
        parent = child.parent.username
        if current_user.is_parent and current_user.username == parent:
            return True
        else:
            return False


class ActionDeleteBase(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Base class for deleting actions. Not to be used on its own."""

    model = None

    def get_queryset(self):
        qs = self.model.objects.filter(
            pk=self.kwargs.get('pk')).select_related(
            'owner', 'owner__user', 'owner__parent')
        return qs

    def get_context_data(self, **kwargs):
        action = self.object
        kwargs['child'] = action.owner
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        action = self.object
        child = action.owner
        child_username = child.user.username
        parent = action.owner.parent.username

        return reverse('dashboard:child_detail',
                       kwargs={'parent': parent,
                               'child_username': child_username,
                               'pk': child.pk})

    def test_func(self):
        """Allow access only to logged in parent user who is parent
        of the child who's action we are deleting.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        action = self.get_object()
        parent = action.owner.parent.username
        if current_user.is_parent and current_user.username == parent:
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


class ActionUpdateBase(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Base class for updating unclaimed smiley and oopsy objects.
    Do not use on its own."""

    model = None
    fields = ('description', 'points')

    def get_context_data(self, **kwargs):
        action = self.object
        kwargs['child'] = action.owner
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        action = self.object
        child = action.owner
        child_username = child.user.username
        parent = action.owner.parent.username

        return reverse('dashboard:child_detail',
                       kwargs={'parent': parent,
                               'child_username': child_username,
                               'pk': child.pk})

    def test_func(self):
        """Allow access only to logged in parent user who is parent
        of the child who's action we are updating.

        Returns
        -------
            Bool
        """
        current_user = self.request.user
        action = self.get_object()
        parent = action.owner.parent.username
        if current_user.is_parent and current_user.username == parent:
            return True
        else:
            return False


class SmileyUpdate(ActionUpdateBase):
    model = Smiley
    template_name = 'dashboard/smiley_update.html'


class OopsyUpdate(ActionUpdateBase):
    model = Oopsy
    template_name = 'dashboard/oopsy_update.html'
