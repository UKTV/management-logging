from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ManagementLoggingReport


urlpatterns = [
    url(r'^$', login_required(ManagementLoggingReport.as_view()), name='management_logging_report'),
]