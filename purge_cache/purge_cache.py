#! /usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import datetime
import requests
import urllib


#-----------------------
bucket = ''
username = ''
password = ''
#-----------------------
separate = ''
suffix_list = []
#-----------------------

count = 0


def httpdate_rfc1123(dt):
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % \
        (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)


def do_http_request(method, key, params=None):
    uri = '/' + bucket + (lambda x: x[0] == '/' and x or '/'+x)(key)
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    uri = urllib.quote(uri)

    length = 0
    dt = httpdate_rfc1123(datetime.datetime.utcnow())
    signature = make_signature(method, uri, dt, length)

    headers = {}
    headers['Date'] = dt
    headers['Authorization'] = signature
    headers['User-Agent'] = "zhanghb-is-here"
    if params != 'g2gCZAAEbmV4dGQAA2VvZg' or 'None':
        headers['x-list-iter'] = params

    URL = "http://v0.api.upyun.com" + uri
    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.session()
    response = session.request(method, URL, headers=headers, timeout=30)
    status = response.status_code
    if status == 200:
        content = response.content
        try:
            iter_header = response.headers['x-upyun-list-iter']
        except Exception as e:
            iter_header = 'g2gCZAAEbmV4dGQAA2VvZg'
        return content + "`" + str(status) + "`" + str(iter_header)
    else:
        print 'status: '+str(status)
        pass


def make_signature(method, uri, date, length):
    sign_string = '&'.join([method, uri, date, str(length), hashlib.md5(password).hexdigest()])
    signature = hashlib.md5(sign_string).hexdigest()
    return 'UpYun ' + username + ':' + signature


def getlist(key='/', params=None):
    content = do_http_request('GET', key, params=params)
    if not content:
        content = 'None`None`None'
    content = content.split("`")
    items = content[0].split('\n')
    content = [dict(zip(['name', 'type', 'size', 'time'],
            x.split('\t'))) for x in items] + content[1].split() + content[2].split()
    return content


def refresh_cache(payload):
    global count
    headers = {'Authorization': 'Basic dXB5dW4uY29tOjEyMzEyM0ZGRkZGRg=='}
    do_refresh = requests.post('http://124.160.114.202:8070/query', data=payload, headers=headers)
    if do_refresh.status_code == 200:
        print payload['query']
        print 'purge success'
        print do_refresh.content
        print count
        count += 1


def print_file(path, params=None):
    global count
    res = getlist(path, params=params)
    for i in res[:-2]:
        try:
            if not i['name']:
                break
            new_path = path + i['name'] if path == '/' else path + '/' + i['name']
            if i['type'] == 'F':
                print_file(new_path)
            else:
                if suffix_list:
                    for suffix in suffix_list:
                        payload = {'option': 'pushpurge', 'query': 'http://'+bucket+'.b0.upaiyun.com'+new_path+separate+suffix}
                        refresh_cache(payload)
                else:
                    payload = {'option': 'pushpurge', 'query': 'http://'+bucket+'.b0.upaiyun.com'+new_path}
                    refresh_cache(payload)
        except Exception as e:
            print 'error message: ---->' + str(e)
            with open('error_file_folder', 'a') as f:
                f.write(path + '\n')

    if res[-1] != 'g2gCZAAEbmV4dGQAA2VvZg':
        print_file(path, res[-1])


def print_file_with_iter(path):
    params = {
        'x-list-iter': None
    }
    return print_file(path, params=params)

if __name__ == '__main__':
    path = raw_input("input path:")
    print_file_with_iter(path)
    print count
