#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
import requests
import re
import json

from argparse import ArgumentParser

DEFAULT_CONFIG_FILE = 'config.json'

def _check(args):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    session = requests.Session()
    session.headers.update(headers)

    with open(DEFAULT_CONFIG_FILE) as config_file:
        config = json.load(config_file)

    websites = config["websites"]

    for site in websites:
        status = session.get(websites[site]).status_code
        print('%-25s %-35s \033[1;32;40m%d\033[0;m' % (site, websites[site], status))

def main():
    usage = '%(prog)s [<args>]'
    description = 'A website checker.'
    parser = ArgumentParser(usage = usage, description = description)

    _check(None)

    return None

if __name__ == '__main__':
    main()
