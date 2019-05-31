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

pre_case = []
pre_recv = None
pre_var = config.custom_var
titledict = {}

def exec_test():
    filename = glob.glob(os.getcwd() + os.sep + '*.xls')[0]
    wb = xlrd.open_workbook(filename)
    for testsheet in config.testcase.keys():
        logr = logger.rstcls.initial(testsheet)
        logl = logger.logcls(testsheet)
        table = wb.sheet_by_name(testsheet)
        title_list = table.row_values(0)
        get_title_index(title_list)
        caselist = get_case(config.testcase[testsheet], table)
        for case_num in caselist:
            api_run(table, int(case_num), logr, logl)


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
    global pre_case, pre_recv, pre_var
    global titledict
    caseinfo = table.row_values(case_num)
    url = caseinfo[titledict["域名IP及端口"]] + caseinfo[titledict["URL_ADDR"]]
    msg = caseinfo[titledict["REQUEST_MESSAGE"]]
    msg_json = json.loads(msg)
    var_list = re.findall(r"\${.*?}", msg)
    if var_list:
        for i in range(len(var_list)):
            var_list[i] = var_list[i].strip("${").strip("}")
        if caseinfo[titledict["前置条件"]]:
            if caseinfo[titledict["前置条件"]] in pre_case:
                pass
            else:
                pre_case.append(int(caseinfo[titledict["前置条件"]]))
                pre_recv = api_run(table, int(caseinfo[titledict["前置条件"]]), logr, logl)
            for pre_condition in var_list:
                if pre_condition not in pre_var.keys():
                    # pre_var[pre_condition] = Check(pre_condition, msg_json)
                    pre_var[pre_condition] = eval("pre_recv" + search_dict(pre_condition, pre_recv))
        for var in var_list:
            if var == "timestamp":
                exec("msg_json" + search_dict(var, msg_json) + "=" + time.time())
            else:
                exec("msg_json" + search_dict(var, msg_json) + "='" + str(pre_var[var]) + "'")
    else:
        if caseinfo[titledict["前置条件"]]:
            if caseinfo[titledict["前置条件"]] in pre_case:
                pass
            else:
                pre_case.append(caseinfo[titledict["前置条件"]])
                pre_recv = json.load(table, caseinfo[titledict["前置条件"]], logr, logl)
    http_test = HTTP_API.HTTP_Cls(table.name)
    recv_msg = http_test.post_msg(url, msg_json)
    pre_case.append(case_num)
    check_flag = check_result(recv_msg, caseinfo)
    print "check_failed: " + str(check_flag)
    if caseinfo[titledict["REMAIN_PARAM"]]:
        remain_param_list = caseinfo[titledict["REMAIN_PARAM"]].split("\n")
        print remain_param_list
        for remain_param in remain_param_list:
            remain_param = remain_param.strip()
            remain_value = find_from_dict(remain_param, recv_msg)
            pre_var[remain_param] = remain_value
    print "pre_var"
    print pre_var
    print "pre_case"
    print pre_case

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
        i = 0
        result_dict = json.loads(caseinfo[titledict["EXPECTED_RESULTS"]])
        # for key in result_dict.keys():
        #     if recv_msg.has_key(key):
        #         print key
        #         i += 1
        #     else:
        #         miss_list.append(key)
        miss_list = compare_dict(result_dict, recv_msg)
        if miss_list:
            return miss_list
    return None




if __name__ == "__main__":
    exec_test()