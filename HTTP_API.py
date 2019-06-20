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
        self.headers = {'Content-Type': 'application/json;charset=UTF-8', 'authorization': 'eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU5MjU0NzcyMH0.JfFdZ8Dqy6YwUR8nXt6Ed_HGtoc7L99FO-PkvdGmMhHON9aVJdQ7mmb5X__neR7pkI7-hM1Mq5rAYuwXxp8gDXQzOSxnbUI4kgMKoJ6olz_IROUwyVK09tO00r6lifkhKQBlTfciBIYA2Kz-qI-y1IxplOwMmcvDnNyj3f-HaY4', 'fronttype': 'scp-admin-ui'}
    # 登陆 data='username=admin&password=YWRtaW4%3D'
    def post_msg(self, url, post_data=None):
        self.r = requests.post(url=url, data=post_data, headers=self.headers)
        print "------ post to %s ------: json_data = %s" % (url, json.dumps(post_data))
        self.log.log("post to %s : json_data = %s" % (url, json.dumps(post_data)))
        if len(self.r.text) < 2000:
            print "-------- recv ---------: %s" % self.r.text
        else:
            print "-------- recv ---------: %s" % "get messege successfully but it's too long to show you !"
        self.log.log("recv : %s" % self.r.text)
        # try:
        #     return self.r.json(), self.r.headers
        # except Exception as e:
        #     return e, self.r.headers
        return self.r.text

    def get_msg(self, url, param=None):
        self.r = requests.get(url=url, params=param, headers=self.headers)
        print "get from %s ------: param = %s, headers = %s" % (url, json.dumps(param), self.headers)
        self.r = requests.get(url=url, params=param, headers=self.headers)
        print "get from %s ------: param = %s" % (url, json.dumps(param))
        self.log.log("get from %s : param = %s" % (url, json.dumps(param)))
        if len(self.r.text) < 2000:
            print "-------- recv ---------: %s" % self.r.text
        else:
            print "-------- recv ---------: %s" % "get messege successfully but it's too long to show you !"
        self.log.log("recv : %s" % self.r.text)
        return self.r.text
        # try:
        #     return self.r.json(), self.r.headers
        # except Exception as e:
        #     if e is ValueError:
        #         return {"code": 200}, self.r.headers
        #     else:
        #         return e, self.r.headers
