from django.views.generic import TemplateView
from accounts.models import Child

# Create your views here.


class HomePage(TemplateView):

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_child:
            print("user is a child")
            kwargs['parent_username'] = Child.objects.get(user=self.request.user).parent.username
            print(kwargs['parent_username'])
        return super().get_context_data(**kwargs)
