from django.views.generic import TemplateView
from django.db import connection

from .models import Logging


class ManagementLoggingReport(TemplateView):
    template_name = 'management_logging_report.html'

    def get_context_data(self, **kwargs):

        cur0 = connection.cursor()
        cur0.execute("select count(distinct class_name) from management_logging_logging")
        has_row0 = cur0.fetchone()

        total_jobs = has_row0[0]

        logging = Logging.objects.all().order_by('name', '-start_datetime')

        jobs = []
        count = 0
        data = []
        for log in logging:
            if log.name not in jobs:
                count += 1
                jobs.append(log.name)
                data.append(log)
            if count == total_jobs:
                break

        return {'data': data}
