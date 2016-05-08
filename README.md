# Version Watcher

Watch new version for something and notify by email when new version detected.

Written in Python 3.

## Requirement

* Python 3
* Python [nvchecker](https://github.com/lilydjwg/nvchecker) package
* Python [requests](https://github.com/kennethreitz/requests) package
* [Maligun](https://www.mailgun.com/) account for sending email
* crontab

Setup on CentOS 7:

```
sudo yum install epel-release
sudo yum install python34
sudo yum install python34-setuptools
sudo easy_install-3.4 pip
sudo pip3 install nvchecker
sudo pip3 install requests
```

## Why not use postfix for sending email?

Since some email service providers (such as Gmail) requires SSL to send email to them, and it's quite complicated to setup with postfix.

## Setup

Create your `config/settings.ini`.

## Crontab

```
# Minute Hour Day Month Day_of_week Command
    0     *    *    *        *      cd /path/to/version-watcher && ./main.py &> log/cron.log
```
