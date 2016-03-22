#!/usr/bin/env python
#-*-coding:utf-8-*-

import httplib
import threading
import time
import requests
from urllib import urlopen
import sys
import re


def getRe(line):
    re1 = '.*?'
    re2 = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'
    rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
    m = rg.search(line)
    if m:
        IPAddress = m.group(1)
        return IPAddress


def taobaoAPI(ip):
    request = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip)
    r = request.json()
    STRING = (r[u'data'][u'ip'] + ":" + r[u'data'][u'country'] + r[u'data'][u'area']
              + r[u'data'][u'city'] + r[u'data'][u'isp']).encode('utf-8')
    return STRING


def getCDN():
    with open('/Users/zhanghb/code/machine_resource/lists_cdn_new', 'r') as f:
        upcdnfile = f.readlines()
    upcdn = []
    for line in upcdnfile:
        if line:
            if line[0:10] == '#60.12.233' or line[0:10] == '#122.224.1' or line[0:10] == '#183.129.2':
                pass
            elif line[0] == '#' and line[-2] == 'P':
                upcdn.append(getRe(line))
    return upcdn


class Purge(threading.Thread):
    def __init__(self, upcdn, target_host, target_uri, expect_headers):
        threading.Thread.__init__(self)
        self.upcdn = upcdn
        self.target_host = target_host
        self.target_uri = target_uri
        self.expect_headers = expect_headers

    def run(self):
        try:
            con = httplib.HTTPConnection(self.upcdn, timeout=50)
            con.connect()
            headers = {
                "Host": self.target_host,
                "User-Agent": "zhanghb-is-here",
            }
            con.request("GET", self.target_uri, None, headers)
            response = con.getresponse()
            resdict = {}
            length = {}
            for h in response.getheaders():
                length[h[0]] = h[1]

            if str(response.status) == '200' and length['content-length'] == self.expect_headers['content-length']:
                oked.append("status: " + str(response.status))
            else:
                err.append("status: " + str(response.status))
            for h in response.getheaders():
                resdict[h[0]] = h[1]
                if str(response.status) == '200' and resdict['content-length'] == self.expect_headers['content-length']:
                    oked.append(h[0] + ": " + h[1])
                else:
                    try:
                        err.append(h[0] + ": " + h[1])
                    except:
                        err.append('error happend')
            if str(response.status) == '200' and length['content-length'] == self.expect_headers['content-length']:
                oked.append("veryfy: " + self.upcdn)
                oked.append("-------------------")
            else:
                err.append("veryfy: " + self.upcdn)
                err.append("-------------------")
        except:
            print sys.exc_info()[1]
            print taobaoAPI(self.upcdn)

    def stop(self):
        self.thread_stop = True


if __name__ == '__main__':
    url = raw_input("请输入需要测试缓存状态的文件地址(http/https开头):")
    target_host = "/".join(url.split("/")[2:3])
    target_uri = "/" + "/".join(url.split("/")[3:])
    content_length = (lambda content_length: content_length or urlopen(url).info().getheader('Content-Length'))\
            (raw_input("输入 content_length 或者回车"))
    expect_headers = {"content-length": content_length}

    oked = []
    err = []
    for upcdn in getCDN():
        purge_test = Purge(upcdn, target_host, target_uri, expect_headers)
        purge_test.start()
        purge_test.stop()
    time.sleep(10)
    for oknode in oked:
        print oknode
    i = 0
    for statusOk in oked:
        if statusOk == 'status: 200':
            i += 1
    j = len(getCDN()) - i
    print
    print "============================================="
    print "     oked = %d failed & timeout = %d " % (i, j)
    print "============================================="
    if j > 0:
        print
        print 'failed node: '
        for up in err:
            print up
