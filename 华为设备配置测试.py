#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   华为设备配置测试
@时间     :   2021-2-4 10:22
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import time
from netmiko import ConnectHandler
import re


def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


def read_file(file_path):
    with open(file_path, 'r', encoding='UTF-8-sig') as file:
        data_str = file.read()
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    data_list = re.split('\n', data_str)
    col_data_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        row_data = row_data.strip('\t')
        row_data = row_data.replace('\t', ' ')
        for col_data in range(row_data.find('  ')):
            row_data = row_data.replace('  ', ' ')
        row_data = re.split(r'[ ,]', row_data)
        if ip_true(row_data[1]):
            col_data_list.append(row_data)
    return col_data_list


def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)


read_file_path = r'D:\xuexi\cheshiwenjian\设备IP地址.txt'
now = time.strftime("%Y%m%d", time.localtime(time.time()))
log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

ip_list = read_file(read_file_path)
SW = {
    'device_type': 'huawei_telnet',
    'username': 'huawei',
    'ip': '',
    'password': "1qaz@WSX"
}

for ip_item in ip_list:
    SW['ip'] = ip_item[1]
    connect = ConnectHandler(**SW)
    log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                  ':' + ip_item[1])

    outcomm = connect.send_config_from_file(
        config_file="comm.txt", cmd_verify=False)
    log_str += '\n##############################\n' + outcomm
    configfile = connect.send_command('dis cu')
    log_str += '\n##############################\n' + configfile
    out_file_path = rf'D:\xuexi\cheshiwenjian\{ip_item[0]}-log.txt'
    output_file(out_file_path, log_str)
    connect.disconnect()
