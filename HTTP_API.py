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
        # self.headers = {'Content-Type': 'application/json'}

    def post_msg(self, url, data=None):
        self.r = requests.post(url=url, json=data)
        print "------ post to %s ------: data = %s" % (url, json.dumps(data))
        self.log.log("post to %s : data = %s" % (url, json.dumps(data)))
        print "-------- recv ---------: %s" % self.r.text
        print "-------- recv_headers --------: %s" % str(self.r.headers)
        self.log.log("recv : %s" % self.r.text)
        self.log.log("recv_headers : %s: " % str(self.r.headers))
        return self.r.json(), self.r.headers

    def get_msg(self, url, param=None):
        self.r = requests.get(url=url, params=param)
        print "get from %s ------: param = %s" % (url, json.dumps(param))
        self.log.log("get from %s : param = %s" % (url, json.dumps(param)))
        print "-------- recv ---------: %s" % self.r.text
        print "-------- recv_headers --------: %s" % str(self.r.headers)
        self.log.log("recv : %s" % self.r.text)
        self.log.log("recv_headers : %s: " % str(self.r.headers))
        try:
            return self.r.json(), self.r.headers
        except ValueError:
            return {"code": 200}, self.r.headers
