#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   网段筛选
@时间     :   2020-4-3 21:53
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here

import re


def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    return data


def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    # data_list = []
    data_list = re.split('\n', data_str)
    return data_list


def col_data_format(data_list, ip_net_mask):
    col_data_list = []
    for row_data in data_list:
        print(type(row_data))
        row_data = re.split(r'/', row_data)
        if ip_true(row_data[0]) and len(row_data) >1:
            if row_data[1] <= ip_net_mask:
                col_data_list.append(row_data[0]+'/'+row_data[1])
    return col_data_list


# 生成文件输出字符串函数
def produce_output_str(data_list):
    output_str = ""
    for data_element in data_list:
        output_str = output_str + str(data_element) + "\n"
    return output_str


# 将文件输出字符串写入文件函数
def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)


def main():
    read_file_path = r'D:\xuexi\cheshiwenjian\哈尔滨城域网未使用IP网段.txt'
    ip_net_mask = '22'
    file_path = r'D:\xuexi\cheshiwenjian\哈尔滨城域网未使用IP网段(22位以上).txt'
    print(f'哈尔滨城域网未使用IP网段({ip_net_mask}位以上)：{file_path}')
    not_use_net_str = read_file(read_file_path)
    not_use_net_list = data_format(not_use_net_str)
    not_use_net_list = col_data_format(not_use_net_list,ip_net_mask)
    not_used_ip_str = produce_output_str(not_use_net_list)
    output_file(file_path, not_used_ip_str)


if __name__ == '__main__':
    main()
