#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   路由提取
@时间     :   2020-4-3 17:25
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re


def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)/\d{1,2}$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
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
            col_data = range(row_data.find('  '))
        row_data = re.split(r' ', row_data)
        # print(row_data)
        if ip_true(row_data[0]) and row_data[1] != 'Static':
            # print(row_data[1])
            col_data_list.append(row_data[0])
    return col_data_list


def main():
    original_file_path = r'D:\xuexi\cheshiwenjian\哈尔滨CR全路由1.txt'

    format_file_path = r'D:\xuexi\cheshiwenjian\哈尔滨CR全路由提取.txt'
    with open(original_file_path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    data_list = data_format(data)
    data_list = col_data_format(data_list)
    # print(data_list)

    data_str = ""
    for data_row in data_list:
        data_str = data_str + str(data_row) + "\n"

    with open(format_file_path, 'w') as file:
        file.write(data_str)

if __name__ == '__main__':
    main()
