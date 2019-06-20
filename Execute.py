# -*- coding:utf-8 -*-
import xlrd
import os
import json
import glob
import config
import re
import HTTP_API
import time
from parse_dict import *
import logger
import sys
import deal_var
from HTML import *
reload(sys)
sys.setdefaultencoding("utf-8")

pre_case_list = []
pre_recv = None
pre_var = config.custom_var
titledict = {}


def exec_test(times=1):
    global pre_case_list, pre_recv, pre_var, titledict
    filename = glob.glob(sys.path[0] + os.sep + '*.xls*')[0]
    wb = xlrd.open_workbook(filename)
    for num in range(times):
        for testsheet in config.test_module.keys():
            pre_case_list = []
            pre_recv = None
            pre_var = config.custom_var
            titledict = {}
            logr = logger.rstcls.initial(testsheet + "_result")
            logl = logger.logcls(testsheet)
            logl.log("Case module : " + testsheet)
            logl.log("Test Round : Round " + str(num + 1))
            logr.log("Case module : " + testsheet)
            logr.log("Test Round : Round " + str(num + 1))
            table = wb.sheet_by_name(testsheet)
            caselist = get_case(config.test_module[testsheet], table)
            for case_num in caselist:
                api_run(table, int(case_num), logr, logl)
            logl.log("Round " + str(num + 1) + " finished")
            logr.log("Round " + str(num + 1) + " finished")


def get_title_index(title_list):
    global titledict
    for title in title_list:
        titledict[title.encode("utf-8")] = title_list.index(title)
    return titledict


def get_case(sheet_list, table):
    case_list = []
    if sheet_list:
        for case_srl in sheet_list:
            if type(case_srl) is int:
                case_list.append(case_srl)
            else:
                extent = case_srl.split('-')
                for i in range(int(extent[0]), int(extent[1])+1):
                    case_list.append(i)
    else:
        case_list = [i + 1 for i in range(table.nrows)]
    return case_list


def api_run(table, case_num, logr, logl):
    global pre_case_list, pre_recv, pre_var
    global titledict
    if not titledict:
        titledict = get_title_index(table.row_values(0))
    print titledict
    caseinfo = table.row_values(case_num)
    modelinfo = (caseinfo, titledict, table, pre_recv, logr, logl)
    url_addr = caseinfo[titledict["URL_ADDR"]]
    url_addr, pre_recv = deal_var.deal_var_nodict(url_addr, modelinfo)
    url = caseinfo[titledict["域名IP及端口"]] + url_addr
    msg = caseinfo[titledict["REQUEST_MESSAGE"]]
    try:
        msg_loads = json.loads(msg)
    except:
        msg_loads = None
    if msg_loads is not None:
        msg_loads, pre_recv = deal_var.deal_var_dict(msg, msg_loads, modelinfo)
    else:
        msg, pre_recv = deal_var.deal_var_nodict(msg, modelinfo)
        msg_loads = msg
    http_test = HTTP_API.HTTP_Cls(table.name)
    if caseinfo[titledict["请求方法"]].upper() == "GET":
        recv_msg, recv_headers = http_test.get_msg(url, msg_loads)
    else:
        recv_msg, recv_headers = http_test.post_msg(url, msg_loads)
    pre_case_list.append(int(case_num))
    try:
        check_flag = check_result(recv_msg, caseinfo)
    except Exception as e:
        check_flag = e
    if check_flag is None:
        print "用例        PASS        %s" % caseinfo[titledict["用例标题"]]
        logr.log("用例        PASS        %s  %s" % (table.name, caseinfo[titledict["用例标题"]]))
        logl.debug("用例        PASS        %s" % caseinfo[titledict["用例标题"]])
    else:
        print "用例        FAIL        %s        fail_result: %s" % (caseinfo[titledict["用例标题"]], str(check_flag))
        logr.log("用例        FAIL        %s  %s        fail_result: %s" % (table.name, caseinfo[titledict["用例标题"]], str(check_flag)))
        logl.debug("用例        FAIL        %s        fail_result: %s" % (caseinfo[titledict["用例标题"]], str(check_flag)))
    # print "check_failed: " + str(check_flag)
    if caseinfo[titledict["REMAIN_PARAM"]]:
        remain_param_list = caseinfo[titledict["REMAIN_PARAM"]].split("\n")
        for remain_param in remain_param_list:
            remain_param = remain_param.strip()
            remain_value = find_from_dict(remain_param, recv_msg)
            pre_var[remain_param] = remain_value
    print "pre_var"
    print pre_var
    print "pre_case_list"
    print pre_case_list
    pre_recv = recv_msg
    return recv_msg


def check_result(recv_msg, caseinfo):
    exp_code = caseinfo[titledict["EXPECTED_CODE"]]
    get_code = find_from_dict("code", recv_msg)
    if exp_code != get_code:
        return "code = " + str(get_code)
    if caseinfo[titledict["EXPECTED_RESULTS"]]:
        result_dict = json.loads(caseinfo[titledict["EXPECTED_RESULTS"]])
        miss_list = compare_dict(result_dict, recv_msg)
        if miss_list:
            return miss_list      # 返回缺少的值
    return None


if __name__ == "__main__":
    exec_test()
    obj = Html(logger.now + "result")
    loglist = []
    for module in config.test_module:
        logfile = obj.find_new_file(os.path.join(os.getcwd(), "log", module))
        loglist.append(logfile)
    obj.parse_logfile(loglist)
