from django.views.generic import TemplateView
from accounts.models import Child

# Create your views here.


class HomePage(TemplateView):

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.is_child:
            kwargs['parent'] = Child.objects.get(
                user=user).parent.username
        return super().get_context_data(**kwargs)
