# Version Watcher

Watch new version of something and notify by email when new version detected.

Written in Python 3.

## Requirement

* Python 3.5+
* Python [nvchecker](https://github.com/lilydjwg/nvchecker) package
* Python [requests](https://github.com/kennethreitz/requests) package
* [Maligun](https://www.mailgun.com/) account for sending email
* crontab

Setup on CentOS 7:

```
# Install Python 3.6 from IUS repository
sudo rpm -Uvh https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install python36u python36u-devel
sudo yum install python36u-setuptools python36u-pip

# Install dependencies
sudo pip3 install nvchecker requests tornado
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
```
