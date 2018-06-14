import pytest

from dashboard.views import DashboardPage
from django.urls import reverse

pytestmark = pytest.mark.django_db
# here we need to find out how to log in a client and access
# child_list for them from request object.


