import sys
import traceback

from rq import Worker


class LoggingWorker(Worker):

    def move_to_failed_queue(self, job, *exc_info):
        exc_string = ''.join(traceback.format_exception(*exc_info))
        self.log.warning('Moving job to {0!r} queue'.format(self.failed_queue.name))
        self.failed_queue.quarantine(job, exc_info=exc_string)
        sys.stderr.write(exc_string)