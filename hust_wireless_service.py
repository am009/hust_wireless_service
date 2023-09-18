#!/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals  # noqa

import re
import sys
import argparse
import datetime
import time
import requests
import os
import subprocess
from contextlib import redirect_stdout
import traceback

platform = os.name # 'posix', 'nt', 'java'

SCHOLL_DNS = '202.114.0.242'

if platform == 'posix':
    QJS_PATH = 'qjs'
elif platform == 'nt':
    QJS_PATH = 'qjs.exe'

RUN_JS_PATH = 'run.js'
# LOG_FILE = r"D:\hust_wireless_auth_service.log"
USERNAME = 'M202271717'
PASSWORD = 'xxxxxxx'

def do_auth():
    print(str(datetime.datetime.now())+': ', end='')
    if not 已经在线():
        if 认证():
            print('认证成功')
            return True
        else:
            return False
    else:
        print('已在线')
        return True

def 已经在线():
    if platform == 'posix':
        return os.system("ping -c 1 "+SCHOLL_DNS + "> /dev/null") == 0
    elif platform == 'nt':
        return os.system("ping -n 1 "+SCHOLL_DNS + "> nul") == 0

def 认证():
    try:
        username = USERNAME
        password = PASSWORD

        result = requests.get('http://www.baidu.com')
        if result.text.find('baidu') != -1:
            print('还是已经在线？: '+ result.text)
            return True
        if result.text.find('eportal') == -1:
            print('认证失败1: '+ result.text)
            return False
        pattarn = re.compile(r"href=.*?\?(.*?)'")
        query_str = pattarn.findall(result.text)[0]

        url = 'http://192.168.50.3:8080/eportal/InterFace.do?method=login'

        post_data = {
            'userId': username,
            'password': 加密(password, query_str),
            'queryString': query_str,
            'service': '',
            'operatorPwd': '',
            'operatorUserId': '',
            'validcode': '',
            'passwordEncrypt': 'true'
        }
        responce = requests.request('POST', url, data=post_data)
        responce.encoding = 'UTF-8'
        res_json = responce.json()

        if res_json['result'] == 'success':
            print('认证成功')
            return True
        else:
            print('认证失败: ' + res_json['message'])
            return False
    except Exception as e:
        traceback.print_exc()
        print("出现异常：没有认证")
        return False

def 加密(password, qstr):
    ind1 = qstr.find('mac=')
    mac = qstr[ind1+4:ind1+36]
    password = password + '>' + mac
    return qjs_enc(password)

def qjs_enc(password):
    if type(password) == str:
        password = password.encode()
    return subprocess.check_output([QJS_PATH, RUN_JS_PATH], input=password, shell=False)


def auth_once():
    ret = False
    while ret != True:
        ret = do_auth()
        sys.stdout.flush()
        time.sleep(5)

if __name__ == '__main__':
    # 判断配置文件存在，长度正确（len>128）
    while True:
        auth_once()
        time.sleep(60)
