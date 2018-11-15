# notifyme

A simple script to watch for a specific phrase in a logfile and send an AWS SNS alert.

## Installation
- Create a virtualenv (out of scope for this doc)
- `pip install -r requirements.txt`
- `cp settings_example.conf settings.conf`
- Customize `settings.conf`

  ```
  [LOCAL]
  HOST = My Server Name

  [AWS]
  SNS_TOPIC = arn:aws:sns:us-east-1:123412341234:mytopic
  AWS_ACCESS_KEY_ID = AKLDSF123513454
  AWS_SECRET_ACCESS_KEY = asdfasdfasdfasdfasdfasdf
  ```
  `HOST` is any name you want to use to identify the server triggering the alert.

## Usage
Pipe any `stdout` into `notifyme.py` and pass the watch phrase as an input arg:
```
tail -f path/to/my/logfile.log | path/to/my/virtualenv/bin/python notifyme.py "Found block"
```

You can also add an optional note to prepend to your notification message:
```
tail -f path/to/my/logfile.log | path/to/my/virtualenv/bin/python notifyme.py "Found block" --note "Nerva"
```

Which yield a notification like:
```
MyServer: Nerva: Found block at height 123456
```

## With `supervisord`
Assuming you already have `supervisord` running, here's an example `/etc/supervisor/conf.d/notifyme.conf`. 
The only noteworthy line is the `command` specification:
```
[program:notifyme]
user=ec2-user
directory=/home/ec2-user/notifyme
command=bash -c "tail -f -n 100 /path/to/my/logfile.log | /home/ec2-user/.virtualenvs/notifyme/bin/python notifyme.py 'Found block'"
autostart=true
autorestart=true
stderr_logfile=/home/ec2-user/notifyme/err.log
stdout_logfile=/home/ec2-user/notifyme/out.log
```
