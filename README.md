# Version Watcher

Watch for new versions and notify by email.

Written in Python 3.

## Requirement

* Python 3.7+
* Python packages:
    * [nvchecker](https://github.com/lilydjwg/nvchecker)
    * [aiohttp](https://pypi.org/project/aiohttp/) (required by nvchecker)
    * [requests](https://github.com/kennethreitz/requests)
* [Maligun](https://www.mailgun.com/) account for sending email
* crontab

Setup on CentOS 8:

```bash
# Install Python 3.11
sudo yum install python3.11 python3.11-pip

# Use venv. Optional
python3 -m venv .venv
source .venv/bin/activate
pip3 install -U pip

# Install pip dependencies
pip3 install -r requirements.txt
```

## Why not use postfix for sending email?

Since some email service providers (such as Gmail) requires SSL to send email to them, and it's quite complicated to setup with postfix.

## Setup

Create `config/settings.ini`, and change `config/nvchecker.ini` as needed.

Run `python3 main.py` to check at once.

Add the following to `crontab` to check regularly:

```
# Minute Hour Day Month Day_of_week Command
    0     *    *    *        *      cd /path/to/version-watcher && ./main.py &>> log/cron.log
# For venv:
#    0     *    *    *        *      cd /path/to/version-watcher && source .venv/bin/activate && ./main.py &>> log/cron.log
```
