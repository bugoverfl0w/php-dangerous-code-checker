#!/bin/bash

[ ! -f /usr/bin/python2.7 ] && echo "please install python2.7" && exit 0
python2.7 get-pip.py
pip2.7 install requests python-dotenv
cp .env.example .env