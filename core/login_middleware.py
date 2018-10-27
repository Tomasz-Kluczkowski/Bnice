import re
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

LOGIN_EXEMPT_URLS = (
    r'^/$',
    r'^/accounts/login/$',
    r'^/accounts/signup/$',
)

if settings.DEBUG:  # pragma: no cover
    LOGIN_EXEMPT_URLS += ('^/__debug__', )


LOGIN_EXEMPT_URLS_RE = [re.compile(url) for url in LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('middleware check login')
        assert hasattr(request, 'user')

        if request.user.is_authenticated:
            return
        if any(url_re.match(request.path) for url_re in LOGIN_EXEMPT_URLS_RE):
            return

        messages.warning(request, 'Please log in to view this page')
        return redirect(f'{settings.LOGIN_URL}?next={request.get_full_path()}')
