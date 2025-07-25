# Version Watcher

Watch for new versions and notify by email.

Written in Python 3.

## Requirement

* Python 3.8+
* [uv](https://docs.astral.sh/uv/)
* Python packages:
    * [nvchecker](https://github.com/lilydjwg/nvchecker)
    * [aiohttp](https://pypi.org/project/aiohttp/) (required by nvchecker)
    * [requests](https://github.com/kennethreitz/requests)
* [Maligun](https://www.mailgun.com/) account for sending email
* crontab

Setup on CentOS 8:

```bash
# Install Python 3.12
sudo yum install python3.12

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

## Why not use postfix for sending email?

Since some email service providers (such as Gmail) requires SSL to send email to them, and it's quite complicated to setup with postfix.

## Setup

Create `config/settings.ini`, and change `config/nvchecker.ini` as needed.

Run `uv run main.py` to check at once.

Add the following to `crontab` to check regularly:

```
# Minute Hour Day Month Day_of_week Command
    0     *    *    *        *      cd /path/to/version-watcher && /path/to/uv run main.py &>> log/cron.log
```
