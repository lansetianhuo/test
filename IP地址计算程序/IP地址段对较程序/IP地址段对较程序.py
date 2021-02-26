#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   IP地址段对较程序
@时间     :   2021-2-26 19:46
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
from IPy import IP, IPSet
import time
import os


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    return data


def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    data_list = data_str.split('\n')
    data_info_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        row_data = row_data.strip('\t')
        data_info_list.append(IP(row_data))
    return data_info_list


def ip_set_agg(data_info_list):
    ip_set_agg = IPSet(data_info_list)
    return ip_set_agg


def out_data_format(ip_set):
    ip_set_str = ""
    for ip_data in ip_set:
        ip_set_str = ip_set_str + str(ip_data) + "\n"
    return ip_set_str


def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)


def main():
    print("请选择IP地址集计算方式：\n"
          "agg:两个地址集求合运算\n"
          "and:两个地址集与运算\n"
          "not:两个地址集非运算\n"
          "in:A为汇总地址集、B为以分配地址集时，求未分配地址段\n"
          "输入q退出！")
    if not os.path.isdir('计算结果'):
        os.mkdir('计算结果')
    while True:
        con_mode = input("请输入掩码转换：")
        if con_mode in ['agg', 'and', 'not', 'in']:
            a_ipset_str_path = r'IP地址集A.txt'
            b_ipset_str_path = r'IP地址集B.txt'
            a_ipset_str = read_file(a_ipset_str_path)
            b_ipset_str = read_file(b_ipset_str_path)

            a_ip_list = data_format(a_ipset_str)
            b_ip_list = data_format(b_ipset_str)
            if con_mode == 'agg':
                agg_ipset = ip_set_agg(a_ip_list + b_ip_list)
                out_results = out_data_format(agg_ipset)
                out_path = r'.\计算结果\合并IP集结果.txt'
                output_file(out_path, out_results)
            elif con_mode == 'and':
                and_ipset = ip_set_agg(a_ip_list) & ip_set_agg(b_ip_list)
                out_results = out_data_format(and_ipset)
                out_path = r'.\计算结果\相同地址段IP集结果.txt'
                output_file(out_path, out_results)
            elif con_mode == 'not':
                a_ip_set = ip_set_agg(a_ip_list)
                b_ip_set = ip_set_agg(b_ip_list)
                and_ip_set = a_ip_set & b_ip_set
                a_ip_set.discard(and_ip_set)
                b_ip_set.discard(and_ip_set)
                a_out_results = out_data_format(a_ip_set)
                out_path = r'.\计算结果\IP地址集A独有地址段.txt'
                output_file(out_path, a_out_results)
                b_out_results = out_data_format(b_ip_set)
                out_path = r'.\计算结果\IP地址集B独有地址段.txt'
                output_file(out_path, b_out_results)
            elif con_mode == 'in':
                a_ip_set = ip_set_agg(a_ip_list)
                b_ip_set = ip_set_agg(b_ip_list)
                and_ip_set = a_ip_set & b_ip_set
                a_ip_set.discard(and_ip_set)
                a_out_results = out_data_format(a_ip_set)
                out_path = r'.\计算结果\IP地址集A未分配地址段.txt'
                output_file(out_path, a_out_results)
            print("计算结束！")
            time.sleep(2)
            break
        elif con_mode in ['q', 'Q']:
            break
        else:
            print("输入参数有误，请根据需要的转换方式输入：agg或and或not或in,输入q退出！")


if __name__ == '__main__':
    main()
