#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Auth:zhanghb、wenjun
# Date:2016-3-14


import requests
import urllib
import Queue
from base64 import b64encode
import getpass

# -----------------------
bucket = raw_input("Please enter your serverName:")
username = raw_input("Please enter your userName:")
password = getpass.getpass("Plaser enter your Password:")
# -----------------------
queue = Queue.LifoQueue()
queue_list = Queue.LifoQueue()


def do_http_request(method, key, upyun_iter):
    uri = '/' + bucket + (lambda x: x[0] == '/' and x or '/' + x)(key)
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    uri = urllib.quote(uri)
    headers = {}
    headers['Authorization'] = "Basic " + b64encode(username + ':' + password)
    headers['User-Agent'] = "zhanghb-is-here"
    headers['X-List-Limit'] = '300'
    if method is not 'DELETE':
        if upyun_iter is not None or upyun_iter is not 'g2gCZAAEbmV4dGQAA2VvZg':
            headers['x-list-iter'] = upyun_iter

    url = "http://v0.api.upyun.com" + uri
    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.session()
    try:
        response = session.request(method, url, headers=headers, timeout=30)
        status = response.status_code
        if status == 200 and method != 'DELETE':
            content = response.content
            try:
                iter_header = response.headers['x-upyun-list-iter']
            except Exception as e:
                iter_header = 'g2gCZAAEbmV4dGQAA2VvZg'
            return content + "`" + str(iter_header)
        elif status == 200 and method == 'DELETE':
            return True
        else:
            print 'status: ' + str(status) + '--->' + url
            print 'message: ' + str(response.headers['X-Error-Code'])
            print 'message: ' + str(response.content)
            with open('delete_failed_list.txt', 'a') as f:
                f.write(uri + '\n' + str(response.headers) + '\n')
            return None
    except Exception as e:
        with open('delete_failed_list.txt', 'a') as f:
            f.write(uri + '---->' + str(e) + '\n')


def getlist(key, upyun_iter):
    content = do_http_request('GET', key, upyun_iter)
    if not content:
        return None
    content = content.split("`")
    items = content[0].split('\n')
    content = [dict(zip(['name', 'type', 'size', 'time'],
                        x.split('\t'))) for x in items] + content[1].split()
    return content


def print_file_with_iter(path):
    upyun_iter = None
    while True:
        while upyun_iter != 'g2gCZAAEbmV4dGQAA2VvZg':
            res = getlist(path, upyun_iter)
            if res:
                upyun_iter = res[-1]
                for i in res[:-1]:
                    try:
                        if not i['name']:
                            if delete_file(path):
                                print 'folder deleted' + path
                            continue
                        new_path = path + i['name'] if path == '/' else path + '/' + i['name']
                        if i['type'] == 'F':
                            queue.put(new_path)
                            queue_list.put(new_path)
                        elif i['type'] == 'N':
                            print new_path
                            result = delete_file(new_path)
                            print 'file deleted--->' + new_path + str(result)
                            with open(bucket + '_file.txt', 'a') as f:
                                f.write(new_path + '\n')
                    except Exception as e:
                        print e
        else:
            if not queue.empty():
                path = queue.get()
                upyun_iter = None
                queue.task_done()
            else:
                while not queue_list.empty():
                    delete_file(queue_list.get())
                    queue_list.task_done()
                break


def delete_file(key):
    return do_http_request('DELETE', key, None)


if __name__ == '__main__':

    if len(str.strip(bucket)) == 0 or len(str.strip(username)) == 0 or len(str.strip(password)) == 0:
        print "401 buket or username and password  is null"
    else:
        path = raw_input('input a path( e.g: "/" ) : ')
        while len(path) == 0:
            path = raw_input('input a path( e.g: "/" ) : ')
        print_file_with_iter(path)
        print "Job's Done!"
