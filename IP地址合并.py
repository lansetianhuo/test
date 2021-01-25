#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   IP地址合并
@时间     :   2021-1-25 10:34
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
from IPy import IP, IPSet


# 判断字符串是否为IP函数
# def ip_true(port_ip):
#     ip_rule = re.compile(
#         '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
#     if ip_rule.match(port_ip):
#         return True
#     else:
#         return False


def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    # data_list = []
    data_list = re.split('\n', data_str)
    return data_list


# def col_data_format(data_list):
#     col_data_list = []
#     for row_data in data_list:
#         row_data = row_data.strip(' ')
#         row_data = row_data.strip('\t')
#         row_data = row_data.replace('\t', ' ')
#         for col_data in range(row_data.find('  ')):
#             row_data = row_data.replace('  ', ' ')
#             # col_data = range(row_data.find('  '))
#         row_data = re.split(r'[ /]', row_data)
#         if ip_true(row_data[0]):
#             col_data_list.append(row_data)
#     return col_data_list


def ip_format(ip_list):
    ip_set = []
    for ip_element in ip_list:
            ip_set.append(IP(ip_element))
    ip_set_agg = IPSet(ip_set)
    return ip_set_agg


def main():
    # ip_str_path = input('IP地址表文件路径：')
    ip_str_path = r'D:\xuexi\cheshiwenjian\平房FW07-地址集-i.txt'

    # ip_set_str_path = input('整合后IP地址集输出文件路径：')
    ip_set_str_path = r'D:\xuexi\cheshiwenjian\合并IP表.txt'
    print(ip_set_str_path)

    with open(ip_str_path, 'r', encoding='utf-8-sig') as file_used_ip:
        ip_list_str = file_used_ip.read()

    ip_list = data_format(ip_list_str)
    ip_set_agg = ip_format(ip_list)
    print(ip_set_agg)


    ip_set_agg_str = ""
    for ip_address_agg in ip_set_agg:
        ip_set_agg_str = ip_set_agg_str + str(ip_address_agg) + "\n"

    with open(ip_set_str_path, 'w') as file_not_used_ip:
        file_not_used_ip.write(ip_set_agg_str)


if __name__ == '__main__':
    main()