#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   从配置分片中提取静态绑定用户数据.py
@时间     :   2020-3-24 16:25
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here

import shelve


def read_data(data_file, data_name):
    data = shelve.open(data_file)
    original_data = data[data_name]
    data.close()
    return original_data


def write_data(file_name, data_name, data):
    stud_db = shelve.open(file_name)
    stud_db[data_name] = data
    stud_db.close()


def static_route_list_collect(dev_data_list):
    static_route_list = []
    for dev_data_row in dev_data_list:
        if len(dev_data_row) > 0:
            if dev_data_row[0].startswith('ip route-static') and not dev_data_row[0].startswith('ip route-static default-preference'):
                static_route_list.append(dev_data_row)
    return static_route_list


def static_routev6_list_collect(dev_data_list):
    static_routev6_list = []
    for dev_data_row in dev_data_list:
        if len(dev_data_row) > 0:
            if dev_data_row[0].startswith('ipv6 route-static') and not dev_data_row[0].startswith('ipv6 route-static default-preference'):
                static_routev6_list.append(dev_data_row)
    return static_routev6_list


def main():
    data_file = r'D:\xuexi\db\dev_data_db'
    read_data_name = 'dev_data_list'
    write_data_name = 'static_route_data_list'
    dev_data_list = read_data(data_file, read_data_name)
    static_route_list = static_route_list_collect(dev_data_list)

    write_data(data_file, write_data_name, static_route_list)

    
    write_datav6_name = 'static_routev6_data_list'
    static_routev6_list = static_routev6_list_collect(dev_data_list)

    write_data(data_file, write_datav6_name, static_routev6_list)


if __name__ == '__main__':
    main()
