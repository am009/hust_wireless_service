#!/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals  # noqa

import re
import sys
import argparse
import datetime
import time
import requests
from contextlib import redirect_stdout

# LOG_FILE = r"D:\hust_wireless_auth_service.log"
USERNAME = 'M202271717'
PASSWORD = 'xxxxxx'

def do_auth():
    # with open(LOG_FILE, 'a') as f:
    #     with redirect_stdout(f):
    print(datetime.datetime.now())
    try:
        result = requests.get('http://www.baidu.com')
    except Exception:
        print('Failed to connect test website!')
        return -1

    if result.text.find('eportal') != -1:
        username = USERNAME
        password = PASSWORD

        pattarn = re.compile(r"href=.*?\?(.*?)'")
        query_str = pattarn.findall(result.text)

        url = 'http://192.168.50.3:8080/eportal/InterFace.do?method=login'
        post_data = {
            'userId': username,
            'password': password,
            'queryString': query_str,
            'service': '',
            'operatorPwd': '',
            'validcode': '',
        }
        responce = requests.request('POST', url, data=post_data)
        responce.encoding = 'UTF-8'
        res_json = responce.json()

        if res_json['result'] == 'fail':
            print(res_json['message'])
        else:
            print('认证成功')
            return 0

    elif result.text.find('baidu') != -1:
        print('已在线')
        return 0
    else:
        print("Opps, something goes wrong!")

def auth_once():
    ret = -1
    while ret != 0:
        ret = do_auth()
        sys.stdout.flush()
        time.sleep(10)

if __name__ == '__main__':
    while True:
        auth_once()
        time.sleep(3600)
