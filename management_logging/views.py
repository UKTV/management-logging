from django.views.generic import TemplateView
from django.db import connection
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import Logging


class ManagementLoggingReport(TemplateView):
    template_name = 'management_logging_report.html'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ManagementLoggingReport, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        data = []

        selected_site = self.request.GET.get('site', None)

        sites = []
        cur0 = connection.cursor()
        cur0.execute("select distinct site from management_logging_logging")
        rows = cur0.fetchall()
        for row in rows:
            sites.append(row[0])

        jobs_names = []
        cur1 = connection.cursor()
        cur1.execute("select distinct class_name from management_logging_logging order by name")
        rows = cur1.fetchall()
        for row in rows:
            jobs_names.append(row[0])

        for job in jobs_names:
            try:
                logs = Logging.objects.filter(
                    class_name=job
                )

                if selected_site != 'None':
                    logs = logs.filter(site=selected_site)

                log = logs.order_by('-start_datetime')[0]
            except IndexError:
                continue
            else:
                data.append(log)

        return {
            'sites': sites,
            'selected_site': selected_site,
            'data': data
        }
