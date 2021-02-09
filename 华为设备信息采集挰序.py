#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   华为设备信息采集挰序
@时间     :   2021-2-7 14:08
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import time
from netmiko import ConnectHandler
import re
import getpass
import huawei_intf_status
from tqdm import tqdm
from time import sleep


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


read_file_path = r'D:\xuexi\cheshiwenjian\华为设备IP地址.txt'
now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

ip_list = read_file(read_file_path)
SW = {
    'device_type': 'huawei_telnet',
    'username': input('设备帐号：'),
    'ip': '',
    'port': '23',
    'password': getpass.getpass('设备密码：')
}
dev_tqdm = tqdm(ip_list, ncols=90)
for ip_item in dev_tqdm:

    SW['ip'] = ip_item[1]
    SW['port'] = ip_item[2]
    connect = ConnectHandler(**SW)
    log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                  ':' + ip_item[1])

    info_col_log = connect.send_command('dis int main', strip_prompt=False,
                                        strip_command=False)
    connect.disconnect()
    log_str += '\n##############################\n' + info_col_log
    logout_file_path = rf'D:\xuexi\cheshiwenjian\{ip_item[0]}-log-{now}.txt'
    output_file(logout_file_path, log_str)

    write_csv_path = rf'D:\xuexi\cheshiwenjian\{ip_item[0]}-{now}.csv'

    huawei_intf_status.inf_status(logout_file_path, write_csv_path)
    sleep(0.1)
    dev_tqdm.set_description('Processing:' + ip_item[0])
