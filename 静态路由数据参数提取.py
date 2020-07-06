#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   静态绑定用户数据参数提取.py
@时间     :   2020-4-5 16:37
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


def static_route_data_collect(static_route_data_set):
    static_route_data_dict_list = []

    # IP地址正则表达式规则
    ip_re = '(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)'
    for static_route_data_list in static_route_data_set:
        static_route_data_dict = {'dest_ip': '', 'ip_mask': '', 'next_hop': '', 'intf_name': '', 'vpn_name': '',
                                  'bfd': '', 'preference': '', 'description': ''}
        intf_name = re.findall(r'(?:{}) (?:{}) (\S*)'.format(ip_re, ip_re, ip_re), static_route_data_list)
        description = re.findall(r'description (\S*)', static_route_data_list)
        route_data = re.findall(r'({})+?'.format(ip_re), static_route_data_list)
        vpn_name = re.findall(r'vpn-instance (\S*) ', static_route_data_list)
        # bfd = re.findall(r'vlan (\d+)(?: qinq )?(\d*)?', static_route_data_list)
        bfd = re.findall(r'bfd-session (\S*)', static_route_data_list)
        preference = re.findall(r'preference (\d{1,3})', static_route_data_list)

        if len(intf_name) > 0:
            if not re.match(r'({})+?'.format(ip_re), intf_name[0]):
                static_route_data_dict['intf_name'] = intf_name[0]
        if len(description) > 0:
            static_route_data_dict['description'] = description[0]
        if len(route_data) > 1:
            static_route_data_dict['dest_ip'] = route_data[0]
            static_route_data_dict['ip_mask'] = route_data[1]
        if len(route_data) > 2:
            static_route_data_dict['next_hop'] = route_data[2]
        if len(vpn_name) > 0:
            static_route_data_dict['vpn_name'] = vpn_name[0]
        if len(bfd) > 0:
            static_route_data_dict['bfd'] = bfd[0]
        if len(preference) > 0:
            static_route_data_dict['preference'] = preference[0]
        static_route_data_dict_list.append(static_route_data_dict)
    return static_route_data_dict_list


def static_routev6_data_collect(static_routev6_data_set):
    static_route_data_dict_list = []
    # IPv6地址正则表达式规则
    ip6_regex = '(?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))'

    for static_routev6_data_list in static_routev6_data_set:
        static_routev6_data_dict = {'dest_ip': '', 'ip_mask': '', 'next_hop': '', 'intf_name': '', 'vpn_name': '',
                                    'bfd': '', 'preference': '', 'description': ''}
        intf_name = re.findall(r'(?:{}) \d+ (\S*)'.format(ip6_regex), static_routev6_data_list)
        description = re.findall(r'description (\S*)', static_routev6_data_list)
        route_data = re.findall(r'({})+?'.format(ip6_regex), static_routev6_data_list)
        ip_mask = re.findall(r'(?:{}) (\d+)'.format(ip6_regex), static_routev6_data_list)
        vpn_name = re.findall(r'vpn-instance (\S*) ', static_routev6_data_list)
        bfd = re.findall(r'bfd-session (\S*)', static_routev6_data_list)
        preference = re.findall(r'preference (\d{1,3})', static_routev6_data_list)

        if len(intf_name) > 0:
            if not re.match(r'({})+?'.format(ip6_regex), intf_name[0]):
                static_routev6_data_dict['intf_name'] = intf_name[0]
        if len(description) > 0:
            static_routev6_data_dict['description'] = description[0]
        if len(route_data) > 0:
            static_routev6_data_dict['dest_ip'] = route_data[0]
        if len(route_data) > 1:
            static_routev6_data_dict['next_hop'] = route_data[1]
        if len(ip_mask) > 0:
            static_routev6_data_dict['ip_mask'] = ip_mask[0]
        if len(vpn_name) > 0:
            static_routev6_data_dict['vpn_name'] = vpn_name[0]
        if len(bfd) > 0:
            static_routev6_data_dict['bfd'] = bfd[0]
        if len(preference) > 0:
            static_routev6_data_dict['preference'] = preference[0]
        static_route_data_dict_list.append(static_routev6_data_dict)

    return static_route_data_dict_list


def main():
    data_file = r'D:\xuexi\db\dev_data_db'
    read_data_name = 'static_route_data_list'
    static_route_data_list = read_data(data_file, read_data_name)

    static_route_data_dict_list = static_route_data_collect(static_route_data_list[0])

    write_data_name = 'static_route_data_dict_list'
    write_data(data_file, write_data_name, static_route_data_dict_list)

    csv_file_name = r'D:\xuexi\db\static_route_data.csv'
    write_csv(csv_file_name, static_route_data_dict_list)

    read_data_name = 'static_routev6_data_list'
    static_routev6_data_list = read_data(data_file, read_data_name)
    static_routev6_data_dict_list = static_routev6_data_collect(static_routev6_data_list[0])

    write_data_name = 'static_routev6_data_dict_list'
    write_data(data_file, write_data_name, static_routev6_data_dict_list)

    csv_file_name = r'D:\xuexi\db\static_routev6_data.csv'
    write_csv(csv_file_name, static_routev6_data_dict_list)


if __name__ == '__main__':
    main()