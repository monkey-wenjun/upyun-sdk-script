#! /usr/bin/env python
# -*- coding: utf-8 -*-


from base64 import b64encode
import requests
import os
import urllib
import time
import getpass

# -----------------------
bucket = raw_input("Please enter your serverName:")
username = raw_input("Please enter your userName:")
password = getpass.getpass("Plaser enter your Password:")
# -----------------------

count = 0
requests_count = 0


def do_http_request(method, key, params, of):
    chunk_size = 8192
    global requests_count
    uri = '/' + bucket + (lambda x: x[0] == '/' and x or '/' + x)(key)
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    uri = urllib.quote(uri)

    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode(username + ':' + password)
    headers['User-Agent'] = "UPYUN_DOWNLOAD_SCRIPT"
    if params is not None:
        if params['x-list-iter'] is not None or not 'g2gCZAAEbmV4dGQAA2VvZg':
            headers['X-List-Iter'] = params['x-list-iter']
    headers['x-list-limit'] = '300'

    URL = "http://v0.api.upyun.com" + uri
    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.session()
    response = session.request(method, URL, headers=headers, timeout=30)
    status = response.status_code
    if status == 200:
        if method == 'GET' and of:
            readsofar = 0
            try:
                total_size = int(response.headers['content-length'])
            except (KeyError, TypeError):
                total_size = 0

            hdr = None
            for chunk in response.iter_content(chunk_size):
                if chunk and hdr:
                    readsofar += len(chunk)
                    if readsofar != total_size:
                        hdr.update(readsofar)
                    else:
                        hdr.finish()
                if not chunk:
                    break
                of.write(chunk)
            return True
        elif method == 'GET' and of is None:

            content = response.content
            try:
                iter_header = response.headers['x-upyun-list-iter']
            except Exception as e:
                iter_header = 'g2gCZAAEbmV4dGQAA2VvZg'
            return content + "`" + str(status) + "`" + str(iter_header)
        elif method == 'HEAD':
            return response.headers['content-length']
    else:
        print 'status: ' + str(status)
        if requests_count == 4:
            requests_count = 0
            with open('download_error.txt', 'a') as f:
                f.write(uri + '\n')
        else:
            requests_count += 1
            time.sleep(1)
            do_http_request('GET', key, params, of=None)


def getlist(key, params):
    content = do_http_request('GET', key, params, of=None)
    if content:
        content = content.split("`")
        items = content[0].split('\n')
        content = [dict(zip(['name', 'type', 'size', 'time'],
                            x.split('\t'))) for x in items] + content[1].split() + content[2].split()
        return content
    else:
        return None


def download_file(path, params):
    global count
    res = getlist(path, params)
    for i in res[:-2]:

        if not i['name']:
            continue
        new_path = path + i['name'] if path == '/' else path + '/' + i['name']
        try:
            if i['type'] == 'F':
                download_file_with_iter(new_path)
            else:
                try:
                    if not os.path.exists(bucket + path):
                        os.makedirs(bucket + path)
                except OSError as e:
                    print 'something wrong when mkdir: ' + str(e)
                save_path = os.getcwd() + '/' + bucket + new_path
                content_length = do_http_request('HEAD', new_path, params=None, of=None)
                if not os.path.isfile(save_path) or os.path.getsize(save_path) == 0 or int(os.path.getsize(
                        save_path)) != int(content_length):
                    with open(save_path, 'wb') as f:
                        download_result = do_http_request('GET', new_path, params=None, of=f)
                        if download_result:
                            count += 1
                            print str(count) + '---->' + save_path
                else:
                    count += 1
                    print str(count) + '----> file already downloaded'
        except Exception as e:
            print str(e)
            with open('download_error.txt', 'a') as f:
                f.write(new_path + '\n')
    if res[-1] != 'g2gCZAAEbmV4dGQAA2VvZg':
        params = {
            'x-list-iter': res[-1]
        }
        download_file(path, params)


def download_file_with_iter(path):
    params = {
        'x-list-iter': None
    }
    return download_file(path, params)


if __name__ == '__main__':
    if len(str.strip(bucket)) == 0 or len(str.strip(username)) == 0 or len(str.strip(password)) == 0:
        print "401 buket or username and password  is null"
    else:
        path = raw_input('input a path( e.g: "/" ) : ')
        while len(path) == 0:
            path = raw_input('input a path( e.g: "/" ) : ')
        download_file_with_iter(path)
        print str(count) + ':Done!'
