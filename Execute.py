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
from HTML import *
reload(sys)
sys.setdefaultencoding("utf-8")

pre_case_list = []
pre_recv = None
pre_var = config.custom_var
titledict = {}


def exec_test(times=1):
    global pre_case_list, pre_recv, pre_var, titledict
    filename = glob.glob(os.getcwd() + os.sep + '*.xls*')[0]
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
            title_list = table.row_values(0)
            get_title_index(title_list)
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
    caseinfo = table.row_values(case_num)
    url = caseinfo[titledict["域名IP及端口"]] + caseinfo[titledict["URL_ADDR"]]
    msg = caseinfo[titledict["REQUEST_MESSAGE"]]
    try:
        msg_json = json.loads(msg)
    except:
        msg_json = None
    var_list = re.findall(r'".*?":\s+?"\${.*?}"', msg)
    key_list = []
    value_list = []
    if var_list:
        for item in var_list:
            value_list.append(item.split("${")[-1].strip('}"'))
            key_list.append(item.split("${")[0].strip('"').strip().strip(':').strip('"'))
        if caseinfo[titledict["前置条件"]]:       # 表格内多个前置条件用空格隔开
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case, logr, logl)
                for pre_condition in var_list:
                    if pre_condition not in pre_var.keys():
                        # pre_var[pre_condition] = Check(pre_condition, msg_json)
                        pre_var[pre_condition] = eval("pre_recv" + search_dict(pre_condition, pre_recv))
        for var in value_list:
            print var_list, key_list, value_list
            var_key = key_list[value_list.index(var)]
            if var == "timestamp":
                exec("msg_json" + search_dict(var_key, msg_json) + "=" + time.time())
            else:
                exec("msg_json" + search_dict(var_key, msg_json) + "='" + str(pre_var[var]) + "'")
    else:
        if caseinfo[titledict["前置条件"]]:
            for pre_case in caseinfo[titledict["前置条件"]].split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = json.load(table, pre_case, logr, logl)
    http_test = HTTP_API.HTTP_Cls(table.name)
    if caseinfo[titledict["请求方法"]].upper() == "GET":
        recv_msg, recv_headers = http_test.get_msg(url, msg_json)
    else:
        recv_msg, recv_headers = http_test.post_msg(url, msg_json)
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
    print "check_failed: " + str(check_flag)
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
    # exp_results = caseinfo[titledict["EXPECTED_RESULTS"]]
    # if exp_results:
    #     exp_results = json.loads(exp_results)
    #     for exp_key, exp_value in exp_results.items():
    #         if exp_value != find_from_dict(exp_key, recv_msg):
    #             return False
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
