# -*- coding:utf-8 -*-


def search_dict(target, temp_dict):  # 返回target在temp_dict中的索引
    for key in temp_dict.keys():
        if key == target:
            return "['" + str(target) + "']"
        else:
            if type(temp_dict[key]) is list:
                temp_dict[key] = temp_dict[key][0]
            if type(temp_dict[key]) is dict:
                return "['" + str(key) + "']" + search_dict(target, temp_dict[key])
    return False


def find_from_dict(target, temp_dict):   # 返回target在temp_dict中的值
    for key in temp_dict.keys():
        if key == target:
            return temp_dict[key]
        else:
            if type(temp_dict[key]) is list:
                temp_dict[key] = temp_dict[key][0]
            if type(temp_dict[key]) is dict:
                return find_from_dict(target, temp_dict[key])
    return False


def compare_dict(dict1, dict2):
    miss_list = []
    for key, value in dict1.items():
        if key in dict2.keys():
            if type(dict2[key]) is list:
                dict2[key] = dict2[key][0]
            if type(dict2[key]) is dict:
                if type(dict1[key]) is dict:
                    miss_list += compare_dict(dict1[key], dict2[key])
        else:
            miss_list.append(key)
    return miss_list

# target = "b"
# mydict = {'a': 1, 'b': {"xy": 4, "xx": 8}, 'c': 3}
# path = search_dict(target, mydict)
# print "mydict" + path + "=24"
# exec("mydict" + path + "=24")
# print mydict
