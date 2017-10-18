#!/usr/bin/env python3
import notify
import logger
import os
import time
import asyncio
from nvchecker import core

class Source(core.Source):
  def on_update(self, name, version, old_version):
    for i in range(3):
      if notify.send_email(name, version, old_version):
        # on update old version if notify success
        oldvers = core.read_verfile(self.oldver)
        oldvers[name] = version
        core.write_verfile(self.oldver, oldvers)
        break
      else:
        time.sleep(3)

def main():
  try:
    s = Source(open('config/nvchecker.ini', 'r'))
    if not os.access(s.oldver, os.W_OK):
      open(s.oldver, 'w').close()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(s.check())
    logger.log('Check finished successfully.')
  except Exception as e:
    logger.log('Check failed.', e, 'error')
    print(time.strftime('%Y-%m-%d %H:%M:%S %z'))
    raise

if __name__ == '__main__':
  main()
