# -*- coding:utf-8 -*-
from Execute import *
import re


# modelinfo = (caseinfo, titledict, table, pre_recv, logr, logl)
def deal_var_dict(msg, msg_loads, modelinfo):
    var_list = re.findall(r'".*?":\s+?"\${.*?}"', msg)
    key_list = []
    value_list = []
    caseinfo, titledict, table, pre_recv, logr, logl = modelinfo
    if var_list:
        for item in var_list:
            value_list.append(item.split("${")[-1].strip('}"'))
            key_list.append(item.split("${")[0].strip('"').strip().strip(':').strip('"'))
        if caseinfo[titledict["前置条件"]]:  # 表格内多个前置条件用空格隔开
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case, logr, logl)
                for pre_condition in value_list:
                    if pre_condition not in pre_var.keys():
                        # pre_var[pre_condition] = Check(pre_condition, msg_loads)
                        pre_var[pre_condition] = eval("pre_recv" + search_dict(pre_condition, pre_recv))
        for var in value_list:
            var_key = key_list[value_list.index(var)]
            if var == "timestamp":
                exec ("msg_loads" + search_dict(var_key, msg_loads) + "=" + time.time())
            else:
                exec ("msg_loads" + search_dict(var_key, msg_loads) + "='" + str(pre_var[var]) + "'")
    else:
        if caseinfo[titledict["前置条件"]]:
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case, logr, logl)
    return msg_loads, pre_recv


def deal_var_nodict(msg, modelinfo):
    caseinfo, titledict, table, pre_recv, logr, logl = modelinfo
    var_list = re.findall(r'"\${(.*?)}"', msg)
    if var_list:
        if caseinfo[titledict["前置条件"]]:
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case, logr, logl)
                for pre_condition in var_list:
                    if pre_condition not in pre_var.keys():
                        # pre_var[pre_condition] = Check(pre_condition, msg_loads)
                        pre_var[pre_condition] = eval("pre_recv" + search_dict(pre_condition, pre_recv))
        for var in var_list:
            msg.replace('"${' + var + '"', pre_var[var])
    else:
        if caseinfo[titledict["前置条件"]]:
            for pre_case in str(caseinfo[titledict["前置条件"]]).split():
                pre_case = int(float(pre_case))
                if pre_case in pre_case_list:
                    pass
                else:
                    pre_case_list.append(pre_case)
                    pre_recv = api_run(table, pre_case, logr, logl)
    return msg, pre_recv