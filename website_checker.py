#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
import requests
import re
import json
import smtplib
import datetime

from argparse import ArgumentParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DEFAULT_CONFIG_FILE = 'config.json'

def _check(args):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    with open(DEFAULT_CONFIG_FILE) as config_file:
        config = json.load(config_file)

    websites = config["websites"]
    sender = config["sender"]
    recipients = config["recipients"]
    msg_body = ''

    for site in websites:
        try:
            res = requests.get(websites[site], headers=headers)
            status = 'OK' if res.status_code == 200 else res.status_code
        except:
            status = 'TIMEOUT'

        result = '%-25s %-35s %10s' % (site, websites[site], status)
        msg_body += result + '\n\r'
        print(result)

    message = MIMEText(msg_body, 'plain', 'utf-8')
    message['Subject'] = "Website daily check - %s" % datetime.datetime.now()
    message['From'] = sender['account']
    message['To'] = ';'.join(recipients)

    if (args.mail):
        try:
            server = smtplib.SMTP(config['host'])
            server.login(sender['account'], sender['password'])
#            server.sendmail(sender['account'], recipients, message.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print(e)


def main():
    usage = '%(prog)s [<args>]'
    description = 'A website checker.'
    parser = ArgumentParser(usage=usage, description=description)

    parser.add_argument('-m', '--mail', action='store_true',
                        help='sent email to recipients')

    args = parser.parse_args()
    _check(args)

    return None

if __name__ == '__main__':
    main()
