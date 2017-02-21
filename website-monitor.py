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

    try:
        config_file = DEFAULT_CONFIG_FILE if not (args.config) else args.config
        with open(config_file) as config_data:
            config = json.load(config_data)
    except:
        print('No such config file.')
        sys.exit(-1)

    websites = config["websites"]
    sender = config["sender"]
    recipients = config["recipients"]
    results = []

    class Result:
        def __init__(self, site, url, status):
            self.site = site
            self.url = url
            self.status = status

        def __str__(self):
            return '%-25s %-35s %10s' % (site, url, status)

        def to_html(self):
            color = 'green' if self.status == 'OK' else 'red'

            return '''<tr style="height: 30px;">
            <td style="width: 25%%;">%s</td>
            <td style="width: 50%%;">%s</td>
            <td style="width: 25%%; color: %s">%s</td>
            </tr>''' % (self.site, self.url, color, self.status)

    now = datetime.datetime.now()
    print(now)

    for site in websites:
        url = websites[site]

        try:
            res = requests.get(websites[site], headers=headers)
            status = 'OK' if res.status_code == 200 else res.status_code
        except:
            status = 'TIMEOUT'

        result = Result(site, url, status)
        results.append(result)
        print(result)

    if (args.mail):
        try:
            msg_body = '<html><body><table>'
            msg_body += '''<thead><tr>
            <th style="width: 30%%">SITE</th>
            <th style="width: 60%%">URL</th>
            <th style="width: 10%%">STATUS</th>
            </tr></thead>'''
            msg_body += '<tbody>%s</tbody>' % ''.join([r.to_html() for r in results])
            msg_body += '</table></body></html>'
            message = MIMEText(msg_body, 'html', 'utf-8')
            message['Subject'] = "Website daily check - %s" % now
            message['From'] = sender['account']
            message['To'] = ';'.join(recipients)

            server = smtplib.SMTP(config['host'])
            server.login(sender['account'], sender['password'])
            server.sendmail(sender['account'], recipients, message.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            print(e)


def main():
    usage = '%(prog)s [<args>]'
    description = 'A website monitor.'
    parser = ArgumentParser(usage=usage, description=description)

    parser.add_argument('-c', '--config', nargs='?',
                        help='specify config file')

    parser.add_argument('-m', '--mail', action='store_true',
                        help='sent email to recipients')

    args = parser.parse_args()
    _check(args)

    return None

if __name__ == '__main__':
    main()
