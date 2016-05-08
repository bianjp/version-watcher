import requests
from config import config
import logger

def send_email(package, version):
  try:
    r = requests.post(
      config['maligun']['api_base_url'] + '/messages',
      timeout = 10,
      auth = ('api', config['maligun']['api_key']),
      data = {
        'from': config['notify']['from'],
        'to': config['notify']['to'],
        'subject': 'Subject: %s has new version %s out' % (package, version),
        'text': 'Hi, %s has new version %s out!' % (package, version),
      }
    )

    if r.ok:
      return True
    else:
      logger.log('Send email failed: %s' % (r.text,), 'error')

  except Exception as e:
    logger.log('Send email failed.', e, 'error')

  return False
