#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   IP包含计算2
@时间     :   2021-1-24 20:46
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
from IPy import IP, IPSet


# 判断字符串是否为IP函数
def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    # data_list = []
    data_list = re.split('\n', data_str)
    return data_list


def col_data_format(data_list):
    col_data_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        row_data = row_data.strip('\t')
        row_data = row_data.replace('\t', ' ')
        for col_data in range(row_data.find('  ')):
            row_data = row_data.replace('  ', ' ')
            # col_data = range(row_data.find('  '))
        row_data = re.split(r'[ /]', row_data)
        if ip_true(row_data[0]):
            col_data_list.append(row_data)
    return col_data_list


def ip_format(ip_list):
    ip_set = []
    for ip_element in ip_list:
        print(ip_element)
        if ip_true(ip_element[0]):
            ip_set.append(IP(ip_element[0]).make_net(ip_element[1]))
    return ip_set


def main():
    # used_ip_str_path = input('被使用IP统计文件路径：')
    used_ip_str_path = r'D:\xuexi\cheshiwenjian\学府FW01-合并IP表.txt'
    print(used_ip_str_path)

    # usable_ip_str_path = input('可用IP范围文件路径：')
    usable_ip_str_path = r'D:\xuexi\cheshiwenjian\平房FW07-合并IP表.txt'
    print(usable_ip_str_path)

    # not_used_ip_str_path = input('未使用IP输出文件路径：')
    not_used_ip_str_path = r'D:\xuexi\cheshiwenjian\学府被包含在学府中IP.txt'
    print(not_used_ip_str_path)

    with open(used_ip_str_path, 'r', encoding='utf-8-sig') as file_used_ip:
        used_ip_str = file_used_ip.read()

    with open(usable_ip_str_path, 'r', encoding='utf-8-sig') as file_usable_ip:
        usable_ip_str = file_usable_ip.read()

    used_ip_list = data_format(used_ip_str)


    usable_ip_list = data_format(usable_ip_str)

    conn_ip = []
    for used_ip in used_ip_list:
        for usable_ip in usable_ip_list:
            if used_ip in IP(usable_ip):
                #print(used_ip,usable_ip)
                conn_ip.append(used_ip)
                break

    # for conn_ip_tmp in conn_ip:
    #     print(conn_ip_tmp)

    not_used_ip_str = ""
    for not_used_ip in conn_ip:
        not_used_ip_str = not_used_ip_str + str(not_used_ip) + "\n"

    with open(not_used_ip_str_path, 'w') as file_not_used_ip:
        file_not_used_ip.write(not_used_ip_str)


if __name__ == '__main__':
    main()