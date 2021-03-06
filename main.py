#!/usr/bin/env python3
import notify
import logger
import os
import time
import asyncio
from nvchecker import core
import logging
import structlog


# Disable nvchecker debug logging
def logger_factory():
    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)
    return _logger


structlog.configure(logger_factory=logger_factory)


class Source(core.Source):
    def on_update(self, name, version, old_version):
        for i in range(3):
            if notify.send_email(name, version, old_version):
                # on update old version if notify success
                old_versions = core.read_verfile(self.oldver)
                old_versions[name] = version
                core.write_verfile(self.oldver, old_versions)
                break
            else:
                time.sleep(3)


def main():
    try:
        s = Source(open('config/nvchecker.ini', 'r'))
        if not os.access(s.oldver, os.W_OK):
            open(s.oldver, 'w').close()
        io_loop = asyncio.get_event_loop()
        io_loop.run_until_complete(s.check())
        logger.log('Check finished successfully.')
    except Exception as e:
        logger.log('Check failed.', e, 'error')
        print(time.strftime('%Y-%m-%d %H:%M:%S %z'))
        raise


if __name__ == '__main__':
    main()
