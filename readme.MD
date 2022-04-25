# todo
> add telegram push + .env

# how to use

```
> ./shell_fapper.py --help
Usage: shell_fapper.py [options]

Options:
  -h, --help            show this help message and exit
  -m MINUTES, --minute=MINUTES
                        -m --minute last modify minutes to check default is                       check all time
  -t TERMINAL, --terminal=TERMINAL
                        -t --terminal show output in terminal default is 0
  -e EMAIL, --email=EMAIL
                        -e --email email result to admins default is 0
  -r REPOS, --repo=REPOS
                        -r --repo repo to check - dir path default is current
                        directory
  -M IF_MODIFY, --send-if-only-modified=IF_MODIFY
                        -M --send-if-only-modify send email if only modified
                        files
```

# example
``` 
./shell_fapper.py -t 1 -m 30 -r ~/git/phpmyadmin/
start check repo /home/quydo/git/phpmyadmin/
/home/quydo/git/phpmyadmin/shell-test.php:shell_exec("rm -rf /tmp/aaa");
--- /home/quydo/git/phpmyadmin/shell-test.php
```

### -t 1 means print to stdout (your screen)
### -m 30: just find files that modified within 30 minutes
### -r ~/git/phpmyadmin: just check this repository code. You can add more repository to check at the same time, ex: ./shell_fapper.py -t 1 -m 30 -r ~/git/phpmyadmin/ -r /tmp/new-repo-to-check

```In the example code, there is dangerous code found```

/home/quydo/git/phpmyadmin/shell-test.php:shell_exec("rm -rf /tmp/aaa");

# variables
### emails: email to receive notification when -e is 1
### if you know you what you do, you can try to change keywords variable

# crontab
### You can set crontab (linux) to monitor your server code, for example every 3 minutes
``` */3 * * * * /path/to/shell-checker.py -e 1 -m 3 -r /path/to/php-repo-1 -r /path/to/php-repo-2```
