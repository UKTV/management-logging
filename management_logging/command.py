import sys

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core.sampling.local.sampler import LocalSampler

from django.core.management.base import BaseCommand, OutputWrapper
from django.utils import timezone

from .models import Logging


class OutputWrapperWithLoggingCapture(object):

    def __init__(self, stream, logging):
        self.bind(stream)
        self.logging = logging

    def write(self, msg, style_func=None, ending=None):
        self.original_stream.write(msg)
        if self.stream == 'stdout':
            self.logging.stdout_output = self.logging.stdout_output + msg
            self.logging.save()
        if self.stream == 'stderr':
            self.logging.stderr_output = self.logging.stderr_output + msg
            self.logging.status = 'Error'
            self.logging.finish_datetime = timezone.now()
            self.logging.save()

    def bind(self, stream):
        self.original_stream = getattr(sys, stream)
        setattr(sys, stream, self)
        self.stream = stream

    def flush(self):
        pass


class CommandwithLogging(BaseCommand):
    help = 'Run all hands off automated tests and log results'
    name = 'Management command test'

    def __init__(self, stdout=None, stderr=None, no_color=False):
        self.logging = Logging.objects.create(
            name=self.name,
            class_name=self.__class__,
            status='Progress'
        )
        stdout = OutputWrapper(stdout or OutputWrapperWithLoggingCapture('stdout', self.logging))
        stderr = OutputWrapper(stderr or OutputWrapperWithLoggingCapture('stderr', self.logging))

        super(CommandwithLogging, self).__init__(stdout=stdout, stderr=stderr, no_color=False)

    def execute(self, *args, **options):
        xray_rules = {
            "version": 2,
            "default": {
                "fixed_target": 1,
                "rate": 1.0
            }
        }
        xray_recorder.configure(
            context_missing='LOG_ERROR', 
            plugins = ('ECSPlugin',),
            sampling_rules=xray_rules,
            sampler=LocalSampler()
        )
        patch_all()
        xray_recorder.begin_segment("CRON")

        super(CommandwithLogging, self).execute(*args, **options)
        self.logging.finish_datetime = timezone.now()
        if self.logging.status == 'Error':
            self.logging.status = 'Warning'
        else:
            self.logging.status = 'Finished'
        self.logging.save()

        xray_recorder.end_segment()