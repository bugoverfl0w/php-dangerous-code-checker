# Features
> Check dangerous code in your php repo
> You can check many repos in the same time
> It is good for monitor your php server code if there is any new/modified not by you (via crontab)

# Install
> bash -x install.sh

# How to use
> update .env file
```sh
TELEGRAM_BOT_TOKEN: telegram bot token
TELEGRAM_CHAT_ID: telegram chat id. How to get your group/channel chat id?
You should add @getidsbot, then it will print your chat id
```

```sh
> ./shell-checker.py -h
Usage: shell-checker.py [options]

Options:
  -h, --help            show this help message and exit
  -m MINUTES, --minute=MINUTES
                        -m --minute last modify minutes to check default is
                        check all time
  -t TERMINAL, --terminal=TERMINAL
                        -t --terminal show output in terminal default is 0
  -n NOTIFY, --notify=NOTIFY
                        -n --notify notify result to telegram default is 0
  -r REPOS, --repo=REPOS
                        -r --repo repo to check - dir path default is current
                        directory
  -M IF_MODIFY, --send-if-only-modified=IF_MODIFY
                        -M --send-if-only-modify send email if only modified

```

# **Example**
``` sh
> ./shell-checker.py -t 1 -n 1 -m 60 -r ~/git/phpmyadmin/
start check repo /home/quydo/git/phpmyadmin/
/home/quydo/git/phpmyadmin/shell-test.php:shell_exec("rm -rf /tmp/aaa");
--- /home/quydo/git/phpmyadmin/shell-test.php

```

```sh
Telegram group message
--------------- /home/quydo/git/phpmyadmin --------------
/home/quydo/git/phpmyadmin/shell-test.php--- shell_exec("rm -rf /tmp/aaa");
------------ modified files ------------
--- /home/quydo/git/phpmyadmin/shell-test.php
```

> -t 1 means print to stdout (your screen)

> -m 60: just find files that modified within 60 minutes

> -n 1: send notification to telegram group/channel

> -r ~/git/phpmyadmin: just check this repository code. You can add more repository to check at the same time, ex: ./shell_fapper.py -t 1 -m 30 -r ~/git/phpmyadmin/ -r /tmp/new-repo-to-check

**In the example code, there is dangerous code found**
```sh
/home/quydo/git/phpmyadmin/shell-test.php:shell_exec("rm -rf /tmp/aaa");
```

# **Variables**
> if you know you what you do, you can try to change keywords variable

# **Crontab**
> You can set crontab (linux) to monitor your server code, for example every 3 minutes
```sh */3 * * * * /path/to/shell-checker.py -t 1 -m 3 -r /path/to/php-repo-1 -r /path/to/php-repo-2```
