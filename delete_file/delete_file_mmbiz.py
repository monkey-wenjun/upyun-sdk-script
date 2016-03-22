#! /usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import urllib
from base64 import b64encode

# -----------------------
bucket = ''
username = ''
password = ''


# -----------------------


def do_http_request(method, key, upyun_iter):
    uri = '/' + bucket + (lambda x: x[0] == '/' and x or '/' + x)(key)
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    uri = urllib.quote(uri)
    headers = {}
    headers['Authorization'] = "Basic " + b64encode(username + ':' + password)
    headers['User-Agent'] = "uptechs/1.0"
    headers['X-List-Limit'] = 100
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
            print 'message:'+ str(response.content)
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
                for i in res[:-1]:
                    if not i['name']:
                        do_http_request('DELETE', path, None)
                        print 'folder deleted' + path
                        continue
                    new_path = path + i['name'] if path == '/' else path + '/' + i['name']
                    if i['type'] == 'F':
                        if do_http_request('DELETE', new_path + '/640', None):
                            if do_http_request('DELETE', new_path, None):
                                print new_path
                        else:
                            if do_http_request('DELETE', new_path, None):
                                print '--->' + new_path
                upyun_iter = res[-1]
            # else:
            #     upyun_iter = 'g2gCZAAEbmV4dGQAA2VvZg'
        else:
            res = getlist(path, upyun_iter)
            try:
                upyun_iter = res[-1]
            except Exception as e:
                break


if __name__ == '__main__':
    path = '/mmbiz'
    print_file_with_iter(path)
    print ": Job's Done!"
