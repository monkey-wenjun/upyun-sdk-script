#! /usr/bin/env python
# -*- coding: utf-8 -*-
# author: support@upyun.com

from base64 import b64encode
import requests
import upyun
import urllib
import Queue

# ----------待拉取的服务名操作员信息-------------
origin_bucket = ''  # (必填) 待拉取的服务名
origin_username = ''  # (必填) 待拉取的服务名下授权的操作员名
origin_password = ''  # (必填) 待拉取服务名下授权操作员的密码
host = ''  # (必填)  待拉取的服务名的访问域名, 请使用 http// 或者 https:// 开头, 比如 'http://techs.upyun.com'
origin_path = '/'  # (必填) 待拉取的资源路径 (默认会拉取根目录下面的所有目录的文件)
# --------------------------------------------

# ----------目标迁移服务名, 操作员信息-------------
target_bucket = ''  # (必填) 文件迁移的目标服务名
target_username = ''  # (必填) 文件迁移的目标服务名的授权操作员名
target_password = ''  # (必填) 文件迁移的目标服务名的授权操作员的密码
save_as_prefix = ''  # (选填) 目标服务名的保存路径的前置路径 (如果不填写, 默认迁移后的路径和原路径相同)
# --------------------------------------------

notify_url = 'http://your_notify_url'  # 将回调地址改成自己的服务器地址, 用来接收又拍云 POST 过来的异步拉取结果

# --------------------------------------------


queue = Queue.LifoQueue()


def push_tasks(url, up):
    fetch_data = [
        {
            'url': host + url,  # 需要拉取文件的 URL
            'random': False,  # 是否追加随机数, 默认 false
            'overwrite': True,  # 是否覆盖，默认 True
            'save_as': url
        }
    ]

    result = up.put_tasks(fetch_data, notify_url, 'spiderman')
    return result


def do_http_request(method, key, upyun_iter):
    uri = '/' + origin_bucket + (lambda x: x[0] == '/' and x or '/' + x)(key)
    if isinstance(uri, unicode):
        uri = uri.encode('utf-8')
    uri = urllib.quote(uri)
    headers = {
        'Authorization': 'Basic ' + b64encode(origin_username + ':' + origin_password),
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


def sort_data(key, upyun_iter):
    result = do_http_request('GET', key, upyun_iter)
    if not result:
        return None
    content = result['content']
    items = content.split('\n')
    content = [dict(zip(['name', 'type', 'size', 'time'],
                        x.split('\t'))) for x in items] + result['iter_header'].split()
    return content


def get_list(path):
    upyun_iter = None
    up = upyun.UpYun(target_bucket, target_username, target_password)
    while True:
        while upyun_iter != 'g2gCZAAEbmV4dGQAA2VvZg':
            res = sort_data(path, upyun_iter)
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
                            print new_path
                            if save_as_prefix:
                                new_path = save_as_prefix + new_path
                                push_tasks(new_path, up)
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


if __name__ == '__main__':
    get_list(origin_path)
