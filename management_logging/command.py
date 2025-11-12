import sys
import uuid

import sentry_sdk

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
        # Create the logging
        self.logging = Logging.objects.create(
            name=self.name,
            class_name=self.__class__,
            status='Progress'
        )
        stdout = OutputWrapper(stdout or OutputWrapperWithLoggingCapture('stdout', self.logging))
        stderr = OutputWrapper(stderr or OutputWrapperWithLoggingCapture('stderr', self.logging))
        super().__init__(stdout=stdout, stderr=stderr, no_color=False)


    def execute(self, *args, **options):
        try:
            # Run the 'handle' method
            super(CommandwithLogging, self).execute(*args, **options)
            # Log the outcome
            self.logging.finish_datetime = timezone.now()
            if self.logging.status == 'Error':
                self.logging.status = 'Warning'
            else:
                self.logging.status = 'Finished'
            self.logging.save()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
        finally:
            sentry_sdk.flush()
