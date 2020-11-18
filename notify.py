import requests
from config import config
import logger


def send_email(package, version, old_version):
    """
    Send email notification on version update

    :param package: Package name
    :param version: New version
    :param old_version: Old version
    :return: Whether email is sent successfully or not
    """
    try:
        r = requests.post(
            config['maligun']['api_base_url'] + '/messages',
            timeout=10,
            auth=('api', config['maligun']['api_key']),
            data={
                'from': config['notify']['from'],
                'to': config['notify']['to'],
                'subject': '%s has new version %s out' % (package, version),
                'text': 'Hi, %s has new version %s out! The previous was %s.' % (package, version, old_version),
            }
        )

        if r.ok:
            return True
        else:
            logger.log('Send email failed: %s' % (r.text,), 'error')

    except Exception as e:
        logger.log('Send email failed.', e, 'error')

    return False
