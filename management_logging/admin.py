from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings

from .models import Logging
from .forms import LoggingForm


class LoggingAdmin(admin.ModelAdmin):
    list_display = ['name', 'status_icon', 'start_datetime', 'finish_datetime']
    list_filter = ('name', 'status', )
    ordering = ('-start_datetime',)
    readonly_fields = ('name', 'status', 'start_datetime', 'finish_datetime',  'class_name', )
    form = LoggingForm
    model = Logging

    def status_icon(self, obj):

        static_url = settings.STATIC_URL
        status = obj.status
        if status == 'Error':
            value = '<img src="{}management_logging/img/icon_error.gif" alt="True">'.format(static_url)
        elif status == 'Finished':
            value = '<img src="{}management_logging/img/icon_success.gif" alt="True">'.format(static_url)
        elif status == 'Progress':
            value = '<img src="{}management_logging/img/icon_progress.gif" alt="True">'.format(static_url)
        return format_html(value)
    status_icon.short_description = 'Status'

    class Media:
        css = {
             'all': ('{}management_logging/css/management_logging.css'.format(settings.STATIC_URL),)
        }


try:
    admin.site.register(Logging, LoggingAdmin)
except admin.sites.AlreadyRegistered:
    pass
