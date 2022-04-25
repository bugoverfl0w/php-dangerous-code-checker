#!/usr/bin/env python2.7
# -*- coding: utf-8 -*- 

# @quydox

import sys, os
import optparse
import subprocess
import requests
from dotenv import dotenv_values

envs = dotenv_values(".env")

class shell:
    author = os.uname()[1]

    # add more dangerous keywords here to search
    keywords = '(`.*`|safe_mode|/etc/passwd|(base64_decode)|shell_exec\(|=exec| exec\(|=system\(| system\(|passthru|readfile|move_uploaded_file|fsockopen|crontab|drop table|drop database|truncate table|mysqldump|crontab|mail\()'

    ignores = '| grep -Ev "(tmp_uploads$|te?mp$|[0-9]$)|.git/*"'

    # minutes to monitor
    minutes = 0

    # find variables
    find_vars = ''

    # messages
    msgs = []
    clis = []

    # repos
    repos = ['./']

    # terminal
    debug = False
    notify = 0
    terminal = 0
    if_modify = 0

    warn = 0
    critical = 0

    # init class
    def __init__(self, debug=False, minutes=0, repos=[], terminal=0, notify=0, if_modify=0):
        self.debug = debug

        if terminal.isdigit() and int(terminal) > 0:
            self.terminal = 1

        if notify.isdigit() and int(notify) > 0:
            self.notify = 1

        # time variables
        if minutes.isdigit() and int(minutes) != 0:
            self.find_vars = '-mmin -%s' % minutes

        if if_modify > 0:
            self.if_modify = 1

        # repositories
        if repos:
            self.repos = repos

    # init variables
    def init_vars(self):
        print 'check cai noi'

    # start check
    def fap(self):
        if not self.repos:
            sys.exit('no repo to check')

        for repo in self.repos:
            self.msgs.append(self.html_color('--------------- %s --------------', 'green') % os.path.abspath(repo))
            print 'start check repo %s' % repo
            self.shell_in_repo(repo)

        if self.terminal:
            for t in self.clis:
                print t

        #print self.msgs
        if self.notify == 1:
            if self.critical > 0:
                self.send_notify()
            else:
                if self.warn > 0 and self.if_modify > 0:
                    self.send_notify()


    # check shell in repo - dir
    def check_shell(self, repo):
        try:
            res = subprocess.check_output("find %s -type f -iname '*.php' %s -print0 | xargs -0 grep -i -EH '%s'" % (repo, self.find_vars, self.keywords), shell=True)
        except:
            return False

        files = []
        messages = {}
        for line in res.splitlines():
            line = line[0:200] # 200 chars
            tmp = line.split(':', 1) # 0 filename 1 messages

            f = tmp[0]
            m = tmp[1]

            self.clis.append('%s:%s' % (f, m))

            if not f in files:
                files.append(f)

            if not messages.has_key(f):
                messages[f] = []

            m = m.replace('<', '|')
            m = m.replace('>', '|')
            m = m.strip()
            m = self.html_color('%0A🥵' + '--- ') + m
            messages[f].append(self.html_color(m, 'blue'))

            self.critical += 1

        tmp = ''
        for f, m in messages.iteritems():
            tmp = tmp + self.html_color(f) +  ''.join(messages[f])

        if len(tmp) > 0:
            #self.msgs.append(tmp + '<br />')
            self.msgs.append(tmp)

    def check_modified_file(self, repo):
        try:
            res_files = subprocess.check_output("find %s -type f -iname '*.php' %s" % (repo, self.find_vars),shell=True)
        except:
            return False

        # new modified files
        if res_files:
            self.msgs.append(self.html_color('------------ modified files ------------', 'aqua'))
            for l in res_files.splitlines():
                self.msgs.append(self.html_color('--- %s' % l, 'red'))
                self.clis.append('--- %s' % l)
                self.warn += 1

    def check_created_dir(self, repo):
        try:
            #print("find %s -type d %s %s" % (repo, self.find_vars, self.ignores))
            res_dirs = subprocess.check_output("find %s -type d %s %s" % (repo, self.find_vars, self.ignores), shell=True)
        except:
            return False

        # new modified directories
        if res_dirs:
            self.msgs.append(self.html_color('------------ folder that have file created ------------', 'aqua'))
            for d in res_dirs.splitlines():
                self.msgs.append(self.html_color('--- %s' % d, 'red'))
                self.clis.append('--- %s' % d)
                self.warn += 1

    def shell_in_repo(self, repo):
        if not os.path.isdir(repo):
            self.msgs.append('dir not exists %s' % self.html_color(repo))
            return False

        self.check_shell(repo)
        self.check_modified_file(repo)
        #self.check_created_dir(repo)

    # fill color msg
    def html_color(self, msg = '', color = 'red'):
        if not msg:
            return False

        #return '<font color="%s">%s</font>' % (color, msg)
        return msg

    # pre html
    def html_pre(self, msg):
        return '<pre>%s</pre>' % msg

    def telegram(self, msg):
        requests.post('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(
            envs['TELEGRAM_BOT_TOKEN'], envs['TELEGRAM_CHAT_ID'], msg
            ))

    def send_notify(self):
        message = '\n'.join(self.msgs)

        self.telegram(message)

# -------------------------------------------------------------------------------
parser = optparse.OptionParser()
parser.add_option('-m', '--minute', action='store', dest='minutes', help='-m --minute last modify minutes to check\ndefault is check all time', default='0')
parser.add_option('-t', '--terminal', action='store', dest='terminal', help='-t --terminal show output in terminal\ndefault is 0', default='0')
parser.add_option('-n', '--notify', action='store', dest='notify', help='-n --notify notify result to telegram\ndefault is 0', default='0')
parser.add_option('-r', '--repo', action='append', dest='repos', help='-r --repo repo to check - dir path\ndefault is current directory', default=[])
parser.add_option('-M', '--send-if-only-modified', action='store', dest='if_modify', help='-M --send-if-only-modify send email if only modified files', default=0)

options, args = parser.parse_args()
repos_, minutes_, terminal_, notify_, if_modify_ = options.repos, options.minutes, options.terminal, options.notify, options.if_modify

fap = shell(repos=repos_, minutes=minutes_, terminal=terminal_, notify=notify_, if_modify=if_modify_)
fap.fap()
