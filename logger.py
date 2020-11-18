import os
import time
import traceback

log_file = 'log/watcher.log'

# create log directory if necessary
if not os.access('log', os.W_OK):
    os.mkdir('log')


def log(msg, exception=None, level='info'):
    if isinstance(exception, str):
        level = exception
        exception = None

    if exception:
        msg += ' ' + traceback.format_exception_only(type(exception), exception)[0]

    file = open(log_file, 'a')
    file.write("[%s] [%s] %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), level, msg.strip()))
    file.close()
