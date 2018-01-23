# coding : UTF-8
__author__ = 'Yuechen'

import json

import requests


# import urllib.request

dictionary = {}


def base_url(mode):
    _base_ = 'http://admin.test.17zuoye.net'
    if mode == 'dev':
        _base_ = 'http://localhost:8085'
    elif mode == 'stg':
        _base_ = 'http://admin.staging.17zuoye.net'
    elif mode == 'prd':
        _base_ = 'http://admin.17zuoye.net'
    return _base_


def read_login_data():
    force_exit = True
    try:
        info = open('valar_morgulis.17zy', 'r')
        _txt_ = info.read()
        global dictionary
        dictionary = json.loads(_txt_)
        force_exit = False
    except FileNotFoundError as ex:
        print(ex.winerror)
    finally:
        info.close()
    return force_exit


def login(_base_, post_data):
    login_uri = '/auth/login.vpage'
    login_url = _base_ + login_uri
    _session_ = requests.Session()
    _session_.post(login_url, data=post_data)
    return _session_


def exchange_group(run_mode, change_group, current_group, date_format):
    if read_login_data():
        return
    global dictionary
    login_data = {"username": dictionary["userName"], "password": dictionary["password"]}
    print("Name:" + login_data['username'] + "  Pwd:" + login_data['password'])

    base = base_url(run_mode)
    session = login(base, login_data)

    # step 1: recover change group if necessary
    enable_req = dictionary["enableGroup"]
    param_enable = {"gid": change_group, "recoveryStudents": True, "fromDate": date_format}
    print(enable_req)
    # res = session.get(base + enable_req, params=param_enable)

    # step 2: exchange group
    exchange_req = dictionary["exchangeGroup"]
    param_exchange = {"nid": change_group, "oid": current_group}
    print(exchange_req)
    # res = session.get(base + exchange_req, params=param_exchange)

    return


if __name__ == '__main__':
    nid = 0
    oid = 0
    dt = '2017123123590000'

    exchange_group('test', nid, oid, dt)
