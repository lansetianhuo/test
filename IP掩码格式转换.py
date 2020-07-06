#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   IP掩码格式转换
@时间     :   2020-4-4 13:47
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
from IPy import IP
import re


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    return data


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


def produce_output_str(data_list):
    output_str = ""
    for data_element in data_list:
        output_str = output_str + str(data_element) + "\n"
    return output_str


def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)


def main():
    file_path = r'D:\xuexi\cheshiwenjian\D设备汇总路由.txt'
    out_file_path = r'D:\xuexi\cheshiwenjian\D设备汇总路由1.txt'
    ip_str = read_file(file_path)
    ip_list = data_format(ip_str).copy()
    ip_list = col_data_format(ip_list).copy()
    ip_set = ip_format(ip_list).copy()
    ip_str = produce_output_str(ip_set)
    output_file(out_file_path, ip_str)


def ip_format(ip_list):
    ip_set = []
    for ip_element in ip_list:
        if ip_true(ip_element[0]):
            ip_set.append(IP(ip_element[0]).make_net(ip_element[1]))
    return ip_set


if __name__ == '__main__':
    main()
