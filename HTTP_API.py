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
        # self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'authorization': 'eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU5Mjg3NzI5NX0.NaFI2zH5ESVdvGJgrNzE63qCWxeWY3ZGnVQJmf7alZjpvPhnITrRFNTv4E6riWLhcWQwHwf_v_p891b1OqM9BcXf3KTkVemDRGPjVxC8zxjiyRc6fEV1ZJ2_aVuHVd2bEzU3wBAiNkLUaEu-DmLsIfPczBPrGJiQ1tT504IgIkA', 'fronttype': 'scp-admin-ui'}
    # 登陆 data='username=admin&password=YWRtaW4%3D'

    def post_msg(self, url, post_data="", headers=None):
        self.r = requests.post(url=url, data=post_data.encode("utf-8"), headers=headers)
        print "------ post to %s ------: data = %s, headers = %s" % (url, json.dumps(post_data), headers)
        self.log.log("post to %s : json_data = %s, headers = %s" % (url, json.dumps(post_data), headers))
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

    def get_msg(self, url, param=None, headers=None):
        self.r = requests.get(url=url, params=param, headers=headers)
        print "------- get from %s ------: param = %s, headers = %s" % (url, json.dumps(param), headers)
        # self.r = requests.get(url=url, params=param, headers=headers)
        # print "get from %s ------: param = %s" % (url, json.dumps(param))
        self.log.log("get from %s : param = %s, headers = %s" % (url, json.dumps(param), headers))
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
