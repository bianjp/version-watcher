#!/usr/bin/env python3
import notify
import logger
import os
import sys
import time
import nvchecker.__main__
import logging
import structlog
import json
from typing import Dict


# Disable nvchecker debug logging
def logger_factory():
    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)
    return _logger


structlog.configure(logger_factory=logger_factory)


def main():
    try:
        sys.argv.append('-c')
        sys.argv.append('config/nvchecker.toml')
        nvchecker.__main__.main()
        old_version_file = 'config/old_ver.json'
        new_version_file = 'config/new_ver.json'
        # nvchecker failed
        if not os.path.exists(new_version_file):
            logger.log('nvchecker execute failed', level='error')
            return
        # The first run
        if not os.path.exists(old_version_file):
            os.rename(new_version_file, old_version_file)
            return

        with open(old_version_file) as old_f, open(new_version_file) as new_f:
            old_versions: Dict[str, str] = json.load(old_f)
            new_versions: Dict[str, str] = json.load(new_f)
            for name in new_versions:
                new_version = new_versions.get(name)
                old_version = old_versions.get(name)
                if not old_version:
                    old_versions[name] = new_version
                elif new_version != old_version:
                    # Only update old version if notify success
                    if notify.send_email(name, new_version, old_version):
                        old_versions[name] = new_version
        with open(old_version_file, 'w') as f:
            json.dump(old_versions, f, ensure_ascii=False, indent=2)
        logger.log('Check finished successfully.')
    except Exception as e:
        logger.log('Check failed.', e, 'error')
        print(time.strftime('%Y-%m-%d %H:%M:%S %z'))
        raise


if __name__ == '__main__':
    main()
