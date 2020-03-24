#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   静态绑定用户数据参数提取.py
@时间     :   2020-3-24 16:37
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
import shelve
import csv


def read_data(data_file, data_name):
    data = shelve.open(data_file)
    original_data = data[data_name]
    data.close()
    return original_data


def write_data(file_name, data_name, data):
    stud_db = shelve.open(file_name)
    stud_db[data_name] = data
    stud_db.close()


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def static_user_data_collect(static_user_data_set):
    static_user_data_dict_list = []

    # IP地址正则表达式规则
    ip_re = '(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)'

    for static_user_data_list in static_user_data_set:
        # static_user_data_dict = {'intf_name': 'none', 'description': 'none', 'ip_list': 'none', 'vpn_name': 'none',
        #                          'gateway': 'none',
        #                          'vlan': 'none', 'domain': 'none'}
        static_user_data_dict = {'intf_name': '', 'description': '', 'ip_list': '', 'vpn_name': '',
                                 'gateway': '',
                                 'vlan': '', 'domain': ''}
        intf_name = re.findall(r'interface (\S*)', static_user_data_list)
        description = re.findall(r'static-user (\S*) ', static_user_data_list)
        ip_list = re.findall(r'({}) ?({})? ?gateway'.format(ip_re, ip_re), static_user_data_list)
        vpn_name = re.findall(r'vpn-instance (\S*) ', static_user_data_list)
        gateway = re.findall(r'gateway ({}) '.format(ip_re), static_user_data_list)
        vlan = re.findall(r'vlan (\d+)(?: qinq )?(\d*)?', static_user_data_list)
        domain = re.findall(r'domain-name (\S*)', static_user_data_list)

        if len(intf_name) > 0:
            static_user_data_dict['intf_name'] = intf_name[0]
        if len(description) > 0:
            ip_rule = re.compile(
                '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
            if not ip_rule.match(description[0]):
                static_user_data_dict['description'] = description[0]
        if len(ip_list) > 0:
            static_user_data_dict['ip_list'] = ip_list[0]
        if len(vpn_name) > 0:
            static_user_data_dict['vpn_name'] = vpn_name[0]
        if len(gateway) > 0:
            static_user_data_dict['gateway'] = gateway[0]
        if len(vlan) > 0:
            static_user_data_dict['vlan'] = vlan[0]
        if len(domain) > 0:
            static_user_data_dict['domain'] = domain[0]
        static_user_data_dict_list.append(static_user_data_dict)
    return static_user_data_dict_list


def main():
    data_file = r'D:\xuexi\db\dev_data_db'
    read_data_name = 'static_user_data_list'
    static_user_data_list = read_data(data_file, read_data_name)

    static_user_data_dict_list = static_user_data_collect(static_user_data_list[0])

    write_data_name = 'static_user_data_dict_list'
    write_data(data_file, write_data_name, static_user_data_dict_list)

    csv_file_name = r'D:\xuexi\db\static_user_data.csv'
    write_csv(csv_file_name, static_user_data_dict_list)


if __name__ == '__main__':
    main()
