import sys
import traceback

from django.db import connections

from rq import Worker


class LoggingWorker(Worker):

    def move_to_failed_queue(self, job, *exc_info):
        exc_string = ''.join(traceback.format_exception(*exc_info))
        self.log.warning('Moving job to {0!r} queue'.format(self.failed_queue.name))
        self.failed_queue.quarantine(job, exc_info=exc_string)
        sys.stderr.write(exc_string)

    def work(self, *args, **kwargs):
        for conn in connections.all():
            conn.close()
        super(LoggingWorker, self).work(*args, **kwargs)