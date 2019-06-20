#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import json
import logger
# import time


class HTTP_Cls(object):
    def __init__(self, arg):
        self.log = logger.logcls(arg)
        self.r = None
        #  application/json;charset=UTF-8
        #  application/x-www-form-urlencoded
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'authorization': 'eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU5MjUyNzA0Mn0.d01UswuNIVSkdExw3a1xFysYUwaG1izsj2-vZpe6oEn7nXUSVLWuZ0Msri7tC9VvKBPrIyFuYb9tdQUCmyucTSm5ToMAYvo9dvshj6Xu_CxR5W-9wXttPDjIPdgoeR03_7gKsApGO_A-VXWm9OrNMMJPFmWGXYqYUgtPGKJHjXg', 'fronttype': 'scp-admin-ui'}
    # 登陆 data='username=admin&password=YWRtaW4%3D'
    def post_msg(self, url, post_data=None):
        self.r = requests.post(url=url, data=post_data, headers=self.headers)
        print "------ post to %s ------: json_data = %s" % (url, json.dumps(post_data))
        self.log.log("post to %s : json_data = %s" % (url, json.dumps(post_data)))
        print "-------- recv ---------: %s" % self.r.text
        print "-------- recv_headers --------: %s" % str(self.r.headers)
        self.log.log("recv : %s" % self.r.text)
        self.log.log("recv_headers : %s: " % str(self.r.headers))
        try:
            return self.r.json(), self.r.headers
        except Exception as e:
            return e, self.r.headers

    def get_msg(self, url, param=None):
        self.r = requests.get(url=url, params=param, headers=self.headers)
        print "get from %s ------: param = %s, headers = %s" % (url, json.dumps(param), self.headers)
        self.r = requests.get(url=url, params=param, headers=self.headers)
        print "get from %s ------: param = %s" % (url, json.dumps(param))
        self.log.log("get from %s : param = %s" % (url, json.dumps(param)))
        print "-------- recv ---------: %s" % self.r.text
        print "-------- recv_headers --------: %s" % str(self.r.headers)
        self.log.log("recv : %s" % self.r.text)
        self.log.log("recv_headers : %s: " % str(self.r.headers))
        try:
            return self.r.json(), self.r.headers
        except Exception as e:
            if e is ValueError:
                return {"code": 200}, self.r.headers
            else:
                return e, self.r.headers
