#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A website monitor.
"""

import sys
import traceback
import requests
import re
import json
import datetime


DEFAULT_CONFIG_FILE = 'config.json'

def check():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    try:
        config_file = DEFAULT_CONFIG_FILE #if not (args.config) else args.config
        with open(config_file) as config_data:
            config = json.load(config_data)
    except:
        return ('Fix your config.')

    websites = config["websites"]
    results = []

    class Result:
        def __init__(self, site, url, status):
            self.site = site
            self.url = url
            self.status = status

        def __str__(self):
            return '%-8s %-25s %-45s' % (status, site, url)

        def to_html(self):
            color = 'green' if self.status == 'OK' else 'red'

            return '''<tr style="height: 30px;">
            <td style="text-align: center; color: %s">%s</td>
            <td>%s</td>
            <td><a href="%s">%s</a></td>
            </tr>''' % (color, self.status, self.site, self.url, self.url)

    now = datetime.datetime.now()
    print(now)

    for site in sorted(websites):
        url = websites[site]

        try:
            res = requests.get(websites[site], headers=headers)
            status = 'OK' if res.status_code == 200 else res.status_code
        except:
            status = 'TIMEOUT'

        result = Result(site, url, status)
        results.append(result)
        print(result)

        body  = "<h3>Site Monitor - %s</h3>" % now
        body += '<table class="table" >'
        body += '''<thead><tr>
        <th style="width: 15%%">STATUS</th>
        <th style="width: 30%%">SITE</th>
        <th style="width: 55%%">URL</th>
        </tr></thead>'''
        body_str = ''.join([r.to_html() for r in sorted(results, key=lambda rst: rst.site)])
        body += '<tbody>%s</tbody>' % body_str
        body += '</table>'
        # test write to file
        # f = open('result.html', 'w')
        # f.write(body)
        # f.close()
        print(body)
    return body

