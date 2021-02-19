#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   file_func
@时间     :   2021-2-19 14:00
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import csv
import os


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def read_file(file_path):
    with open(file_path, 'r', encoding='UTF-8-sig') as file:
        data = file.read()
        data.strip('\n')
    return data


def sum_write_csv(sum_csv_path, write_csv_path_list):
    header = [
        '设备名',
        '设备IP',
        '端口名',
        '管理状态',
        '物理状态',
        '协议状态',
        '端口描述',
        '带宽',
        '模块类型',
        '模块距离',
        '收光',
        '收光范围',
        '发光',
        '发光范围',
        '入流量%',
        '出流量%',
        '收光状态',
        '设备厂商']
    with open(sum_csv_path, 'a', encoding='utf-8-sig', newline='') as wf:
        writer = csv.writer(wf, dialect='excel')
        writer.writerow(header)
    for table_name in write_csv_path_list:
        if os.path.isfile(table_name):
            with open(table_name, encoding='utf-8-sig') as readfile:
                read_data = csv.DictReader(readfile)
                read_rows = [read_row for read_row in read_data]
            with open(sum_csv_path, 'a', encoding='utf-8-sig', newline='') as writefile:
                file_dict = csv.DictWriter(writefile, header, dialect="excel")
                file_dict.writerows(read_rows)
                #
