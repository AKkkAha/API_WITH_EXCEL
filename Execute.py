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
logr = None
logl = None


def exec_test(times=1):
    global pre_case_list, pre_recv, pre_var, titledict, logr, logl
    #add by zx---begin
    # global my_token
    # my_token = None
    # add by zx---end
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
                api_run(table, int(case_num))
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

def make_headers_json(header_str):
    """
    :param header_str: 从chrome控制台直接复制出来的headers外面用单引号
    :return: json_str
    """
    headers_li = header_str.split('\n')
    header_ch = []

    for each in headers_li:
        each = each.replace(' ', '', 1)
        each_li = each.split(':', 1)
        each_li[0] = "\'" + each_li[0] + "\':"
        each_li[1] = "\'" + each_li[1] + "\',\n"
        each_str = ''.join(each_li)
        header_ch.append(each_str)
    all_str = ''.join(header_ch)
    headers = json.dumps(eval('{' + all_str[:-3] + '}'))

    return headers

def api_run(table, case_num):
    print "run case " + str(case_num)
    global pre_case_list, pre_recv, pre_var, logr, logl
    global titledict
    global my_token
    if not titledict:
        titledict = get_title_index(table.row_values(0))
    caseinfo = table.row_values(case_num)
    url_addr = caseinfo[titledict["URL_ADDR"]]
    url_addr = deal_var(url_addr, caseinfo, table)
    url = caseinfo[titledict["域名IP及端口"]] + url_addr
    msg = caseinfo[titledict["REQUEST_MESSAGE"]]
    try:
        msg_loads = json.loads(msg)
    except:
        msg_loads = None
    if type(msg_loads) is dict:
        msg = deal_var(msg, caseinfo, table)
    else:
        msg = deal_var(str(msg), caseinfo, table)
    http_test = HTTP_API.HTTP_Cls(table.name)
    # add by zx---begin
    # if my_token:
    #     http_test.headers["authorization"] = my_token
    #     print("header is set by token={}".format(http_test.headers))
    # if case_num in (4,5):
    #     http_test.headers["Content-Type"] = "application/json;charset=UTF-8"
    #     print("header is set by case {0}={1}".format(case_num, http_test.headers))
    # add by zx---end
    headers = caseinfo[titledict["HEADERS"]]
    headers = make_headers_json(headers.encode('utf-8'))
    headers = json.loads(deal_var(headers, caseinfo, table))
    if caseinfo[titledict["请求方法"]].upper() == "GET":
        recv_msg = http_test.get_msg(url, msg, headers)
    else:
        recv_msg = http_test.post_msg(url, msg, headers)
    #add by zx---begin
    # if "token" in recv_msg:
    #     dict_tmp = eval(recv_msg)
    #     if "data" in dict_tmp and "token" in dict_tmp["data"]:
    #         my_token = dict_tmp["data"]["token"]
    #         print("my_token set to:{}".format(my_token))
    #add by zx---end
    if int(case_num) not in pre_case_list:
        pre_case_list.append(int(case_num))
    check_flag = check_result(recv_msg, caseinfo)
    if check_flag is None:
        print "用例        PASS        %s" % caseinfo[titledict["用例标题"]]
        logr.log("用例        PASS        %s  %s" % (table.name, caseinfo[titledict["用例标题"]]))
        logl.debug("用例        PASS        %s" % caseinfo[titledict["用例标题"]])
    else:
        print "用例        FAIL        %s        fail_result: %s" % (caseinfo[titledict["用例标题"]], str(check_flag))
        logr.log("用例        FAIL        %s  %s        fail_result: %s" % (table.name, caseinfo[titledict["用例标题"]], str(check_flag)))
        logl.debug("用例        FAIL        %s        fail_result: %s" % (caseinfo[titledict["用例标题"]], str(check_flag)))
    # print "check_failed: " + str(check_flag)
    try:
        recv_msg = json.loads(recv_msg)
        pre_recv =recv_msg
    except:
        pass
    if caseinfo[titledict["REMAIN_PARAM"]]:
        remain_param_list = caseinfo[titledict["REMAIN_PARAM"]].split()
        for remain_param in remain_param_list:
            remain_param = remain_param.strip()
            remain_value = find_from_dict(remain_param, recv_msg)
            pre_var[remain_param+'_'+str(case_num)] = remain_value
    print "pre_var"
    print pre_var
    print "pre_case_list"
    print pre_case_list
    return recv_msg


# def deal_var_dict(msg, msg_loads, caseinfo, table):
#     global pre_recv
#     var_list = re.findall(r'".*?":\s+?"\${.*?}"', msg)
#     key_list = []
#     value_list = []
#     if var_list:
#         for item in var_list:
#             value_list.append(item.split("${")[-1].strip('}"'))
#             key_list.append(item.split("${")[0].strip('"').strip().strip(':').strip('"'))
#         if caseinfo[titledict["前置条件"]]:  # 表格内多个前置条件用空格隔开
#             for pre_case in str(caseinfo[titledict["前置条件"]]).split():
#                 pre_case = int(float(pre_case))
#                 if pre_case in pre_case_list:
#                     pass
#                 else:
#                     pre_case_list.append(pre_case)
#                     pre_recv = api_run(table, pre_case)
#                 for pre_condition in value_list:
#                     if pre_condition not in pre_var.keys():
#                         # pre_var[pre_condition] = Check(pre_condition, msg_loads)
#                         pre_var[pre_condition] = eval("pre_recv" + search_dict(pre_condition, pre_recv))
#         for var in value_list:
#             var_key = key_list[value_list.index(var)]
#             if var == "timestamp":
#                 exec ("msg_loads" + search_dict(var_key, msg_loads) + "=" + time.time())
#             else:
#                 exec ("msg_loads" + search_dict(var_key, msg_loads) + "='" + str(pre_var[var]) + "'")
#     else:
#         if caseinfo[titledict["前置条件"]]:
#             for pre_case in str(caseinfo[titledict["前置条件"]]).split():
#                 pre_case = int(float(pre_case))
#                 if pre_case in pre_case_list:
#                     pass
#                 else:
#                     pre_case_list.append(pre_case)
#                     pre_recv = api_run(table, pre_case)
#     return msg_loads


def deal_var(msg, caseinfo, table):
    global pre_recv
    var_list = re.findall(r'\${(.*?)}', msg)
    if var_list:
        if caseinfo[titledict["前置条件"]]:
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case)
                for pre_condition in var_list:
                    if pre_condition not in pre_var.keys():
                        # pre_var[pre_condition] = Check(pre_condition, msg_loads)
                        pre_var[pre_condition] = eval("pre_recv" + search_dict(pre_condition, pre_recv))
        for var in var_list:
            msg = msg.replace('${' + str(var) + '}', pre_var[var])
    else:
        if caseinfo[titledict["前置条件"]]:
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                print("pre_case={}".format(pre_case))
                print("pre_case_list={}".format(pre_case_list))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case)
                    print("pre_recv={}".format(pre_recv))
    return str(msg)


def check_result(recv_msg, caseinfo):
    try:
        recv_msg = json.loads(recv_msg)
        exp_code = caseinfo[titledict["EXPECTED_CODE"]]
        if exp_code:
            get_code = find_from_dict("code", recv_msg)
            if exp_code != get_code:
                return "code = " + str(get_code)
        if caseinfo[titledict["EXPECTED_RESULTS"]]:
            try:
                result_dict = json.loads(caseinfo[titledict["EXPECTED_RESULTS"]])
                miss_list = compare_dict(result_dict, recv_msg)
                if miss_list:
                    return miss_list  # 返回缺少的值
            except:
                result = json.loads(caseinfo[titledict["EXPECTED_RESULTS"]])
                if recv_msg != result:
                    return recv_msg
    except:
        if caseinfo[titledict["EXPECTED_RESULTS"]]:
            try:
                json.loads(caseinfo[titledict["EXPECTED_RESULTS"]])
                return recv_msg
            except:
                result = str(caseinfo[titledict["EXPECTED_RESULTS"]])
                if recv_msg != result:
                    return recv_msg
    return None


if __name__ == "__main__":
    exec_test()
    obj = Html(logger.now + "result")
    loglist = []
    for module in config.test_module:
        logfile = obj.find_new_file(os.path.join(os.getcwd(), "log", module))
        loglist.append(logfile)
    obj.parse_logfile(loglist)
