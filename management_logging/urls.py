from django.urls import re_path
from django.contrib.auth.decorators import login_required

from .views import ManagementLoggingReport


urlpatterns = [
    re_path(r'^$', login_required(ManagementLoggingReport.as_view()), name='management_logging_report'),
]
