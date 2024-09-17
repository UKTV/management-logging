from django import forms
from django.utils.html import format_html

from .models import Logging


class OutputWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        try:
            return format_html('<pre><div class="grp-readonly management-output">{}</div></pre>'.format(value))
        except Exception:
            return '<pre><div class="grp-readonly management-output">{}</div></pre>'.format(value)


class LoggingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoggingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['stdout_output'].widget = OutputWidget()
            self.fields['stderr_output'].widget = OutputWidget()

    class Meta:
        model = Logging
        fields = '__all__'

