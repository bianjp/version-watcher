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


def read_old_versions(file: str) -> Dict[str, str]:
    # The first run
    if not os.path.exists(file):
        return {}
    with open(file) as f:
        return json.load(f)


def read_new_versions(file: str) -> Dict[str, str]:
    with open(file) as f:
        data: Dict[str, Dict[str, str]] = json.load(f).get('data')
        return dict([(k, v.get('version')) for k, v in data.items() if v and v.get('version')])


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

        old_versions = read_old_versions(old_version_file)
        new_versions = read_new_versions(new_version_file)

        need_update = False
        for name in new_versions:
            new_version = new_versions.get(name)
            old_version = old_versions.get(name)
            if not old_version:
                old_versions[name] = new_version
                need_update = True
            elif new_version != old_version:
                # Only update old version if notify success
                if notify.send_email(name, new_version, old_version):
                    old_versions[name] = new_version
                    need_update = True
        if need_update:
            with open(old_version_file, 'w') as f:
                json.dump(old_versions, f, ensure_ascii=False, indent=2)
        logger.log('Check finished successfully.')
    except Exception as e:
        logger.log('Check failed.', e, 'error')
        print(time.strftime('%Y-%m-%d %H:%M:%S %z'))
        raise


if __name__ == '__main__':
    main()
