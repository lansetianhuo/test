#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   城域网未使用IP地址网段查找v4
@时间     :   2020-4-3 20:35
@作者     :   lansetianhuo
@版本     :   5.0
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


# 判断字符串是否为IP网段函数
def ip_net_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)/\d{1,2}$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


# 将读入的文件字符串以回车为分隔符，分隔成列表
def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    # data_list = []
    data_list = re.split('\n', data_str)
    return data_list


# 将分隔后的列表纯化，以空格或/为分隔符进一步分隔成二维列表
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


# 将二维列表中第一个元素为IP地址的列表的前两个元素通过IPy模块中的IP函数组成IP类型数据
def ip_format(ip_list):
    ip_set = []
    for ip_element in ip_list:
        if ip_true(ip_element[0]):
            ip_set.append(IP(ip_element[0]).make_net(ip_element[1]))
    return ip_set


# 从城域网CR路由原表文件读取数据并纯化存成二维列表，将第一个元素为IP网段的列表存入col_data_list列表中.
# 并输出城域网CR路由表清理后文件
def format_routing_table(original_file_path, format_file_path):
    data = read_file(original_file_path)
    data_list = data_format(data)
    col_data_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        for col_data in range(row_data.find('  ')):
            row_data = row_data.replace('  ', ' ')
        row_data = re.split(r' ', row_data)
        if ip_net_true(row_data[0]):
            col_data_list.append(row_data)

    data_str = produce_output_str(col_data_list)
    output_file(format_file_path, data_str)
    return col_data_list


# 在路由表中比对可用IP网段集，提取本城域网内已使用路由
def extract_used_ip(routing_table, usable_ip_set):
    extract_used_ip_list = []
    for route_ip in routing_table:
        for usable_ip in usable_ip_set:
            if route_ip[0] in usable_ip:
                if IP(route_ip[0]) != usable_ip:
                    extract_used_ip_list.append(route_ip[0])
                elif IP(route_ip[0]) == usable_ip and route_ip[-2] != '202.97.32.185':
                    extract_used_ip_list.append(route_ip[0])
    return extract_used_ip_list


# 读文件函数
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    return data


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


# 按掩码长度过滤出IP地址网段
def ip_mask_filter(data_list, ip_mask_len):
    ip_data_list = []
    for row_data in data_list:
        row_data_list = str(row_data).split(r'/')
        if ip_true(row_data_list[0]) and len(row_data_list) > 1:
            if row_data_list[1] <= ip_mask_len:
                ip_data_list.append(row_data)
    return ip_data_list


def main():
    original_file_path = r'D:\xuexi\cheshiwenjian\哈尔滨CR全路由表.txt'
    print(f'城域网CR路由原表文件路径：{original_file_path}')

    format_file_path = r'D:\xuexi\cheshiwenjian\哈尔滨CR全路清理后文件.txt'
    print(f'城域网CR路由表清理后文件路径：{format_file_path}')

    # usable_ip_str_path = r'D:\xuexi\cheshiwenjian\哈尔滨城域网可用汇总路由.txt'
    usable_ip_str_path = r'D:\xuexi\cheshiwenjian\D设备汇总路由.txt'
    print(f'城域网可用IP网段存放文件路径：{usable_ip_str_path}')

    used_ip_str_path = r'D:\xuexi\cheshiwenjian\哈尔滨城域网已使用IP网段.txt'
    print(f'城域网已使用IP网段存放文件路径：{used_ip_str_path}')

    not_used_ip_str_path = r'D:\xuexi\cheshiwenjian\哈尔滨城域网未使用IP网段.txt'
    print(f'城域网未使用IP网段存放文件路径：{not_used_ip_str_path}')

    ip_net_mask = '24'
    not_used_ip_mask_str_path = r'D:\xuexi\cheshiwenjian\哈尔滨城域网未使用IP网段({}位以上).txt'.format(ip_net_mask)
    print(f'哈尔滨城域网未使用IP网段({ip_net_mask}位以上)：{not_used_ip_mask_str_path}')

    usable_ip_str = read_file(usable_ip_str_path)
    usable_ip_list = data_format(usable_ip_str).copy()
    usable_ip_list = col_data_format(usable_ip_list).copy()
    usable_ip_set = ip_format(usable_ip_list).copy()

    conn_ip = IPSet(usable_ip_set)

    route_ip_list = format_routing_table(original_file_path, format_file_path).copy()
    used_ip_list = extract_used_ip(route_ip_list, usable_ip_set).copy()
    used_ip_str = produce_output_str(used_ip_list)
    output_file(used_ip_str_path, used_ip_str)

    used_ip_list = col_data_format(used_ip_list).copy()
    used_ip_net_set = ip_format(used_ip_list).copy()

    # 用已使用地址从可用IP地址集中算出未使用地址
    for used_ip_net in used_ip_net_set:
        conn_ip.discard(IP(used_ip_net))

    not_used_ip_str = produce_output_str(conn_ip)
    output_file(not_used_ip_str_path, not_used_ip_str)

    not_used_ip_filter_list = ip_mask_filter(conn_ip, ip_net_mask).copy()
    not_used_ip_filter_str = produce_output_str(not_used_ip_filter_list)
    output_file(not_used_ip_mask_str_path, not_used_ip_filter_str)


if __name__ == '__main__':
    main()
