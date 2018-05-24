#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from base64 import b64encode
import requests
import urllib
import Queue

# -----------------------
bucket = ''
username = ''
password = ''

path = '/'
# -----------------------

queue = Queue.LifoQueue()


def do_http_request(method, key, upyun_iter):
    uri = '/' + bucket + (lambda x: x[0] == '/' and x or '/' + x)(key)
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    uri = urllib.quote(uri)
    headers = {
        'Authorization': 'Basic ' + b64encode(username + ':' + password),
        'User-Agent': 'up-python-script',
        'X-List-Limit': '300'
    }
    if upyun_iter is not None or upyun_iter is not 'g2gCZAAEbmV4dGQAA2VvZg':
        headers['x-list-iter'] = upyun_iter

    url = "http://v0.api.upyun.com" + uri
    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.session()
    try:
        response = session.request(method, url, headers=headers, timeout=30)
        status = response.status_code
        if status == 200:
            content = response.content
            try:
                iter_header = response.headers['x-upyun-list-iter']
            except Exception as e:
                iter_header = 'g2gCZAAEbmV4dGQAA2VvZg'
            data = {
                'content': content,
                'iter_header': iter_header
            }
            return data
        else:
            return None
    except Exception as e:
        return None


def getlist(key, upyun_iter):
    result = do_http_request('GET', key, upyun_iter)
    if not result:
        return None
    content = result['content']
    items = content.split('\n')
    content = [dict(zip(['name', 'type', 'size', 'time'],
                        x.split('\t'))) for x in items] + result['iter_header'].split()
    return content


def count_dir_size(path):
    upyun_iter = None
    size = 0
    while True:
        while upyun_iter != 'g2gCZAAEbmV4dGQAA2VvZg':
            res = getlist(path, upyun_iter)
            if res:
                upyun_iter = res[-1]
                for i in res[:-1]:
                    try:
                        if not i['name']:
                            continue
                        new_path = path + i['name'] if path == '/' else path + '/' + i['name']
                        if i['type'] == 'F':
                            queue.put(new_path)
                        elif i['type'] == 'N':
                            print 'size ++ ----> {0} B'.format(size)
                            size += int(i['size'])
                    except Exception as e:
                        print e
            else:
                if not queue.empty():
                    path = queue.get()
                    upyun_iter = None
                    queue.task_done()
        else:
            if not queue.empty():
                path = queue.get()
                upyun_iter = None
                queue.task_done()
            else:
                break
    return size / 1024 / 1024 / 1024


if __name__ == '__main__':
    size = count_dir_size(path)
    print "Job's Done!"
    print 'your path: "{0}" , total size: "{1}" GB'.format(path, size)
