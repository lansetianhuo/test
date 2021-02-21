#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   网络设备配置保存
@时间     :   2021-2-21 15:27
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import getpass
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
# import logging

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


def huawei_configfile_collect(ip_item, dev_list):
    if ip_item[3] == 'telnet':
        dev_list['device_type'] = 'huawei_telnet'
    elif ip_item[3] == 'ssh':
        dev_list['device_type'] = 'huawei'

    c_start_time = time.time()
    print(
        f'{ip_item[0]}:操作开始！时间{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c_start_time))}.')
    try:
        connect = ConnectHandler(**dev_list)
    except NetmikoAuthenticationException:  # 认证失败报错记录
        print(ip_item[0], '认证失败！')
        connect_err = open(rf'.\登录错误日志\{ip_item[0]}_登录错误_{now}.txt', 'a')
        connect_err.write(ip_item[0] + ':认证失败!！\n')
        connect_err.close()
    except NetmikoTimeoutException:  # 登录超时报错记录
        print(ip_item[0], '连接超时！')
        connect_err = open(rf'.\登录错误日志\{ip_item[0]}_登录错误_{now}.txt', 'a')
        connect_err.write(ip_item[0] + ':连接超时！\n')
        connect_err.close()
    except ConnectionRefusedError:  # 拒绝连接报错记录
        print(ip_item[0], '拒绝连接！')
        connect_err = open(rf'.\登录错误日志\{ip_item[0]}_登录错误_{now}.txt', 'a')
        connect_err.write(ip_item[0] + ':拒绝连接！\n')
        connect_err.close()
    else:
        # logging.basicConfig(filename=rf".\操作日志{now}\{ip_item[0]}-log-{now}.txt", level=logging.DEBUG)
        hostname = connect.send_command(
            'display current-configuration | include sysname')[8:]
        job_col = connect.send_command_timing('save') + '\n'
        job_col += connect.send_command_timing('y', strip_prompt=False, strip_command=False)
        connect.disconnect()
        c_end_time = time.time()
        print(f'{ip_item[0]}:操作完成！耗时{c_end_time - c_start_time:.3f}秒')
        log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                      ':' + ip_item[1] + ':' + dev_list['port'])
        log_str += '\n##############################\n' + job_col
        logout_file_path = rf'.\操作日志{now}\{hostname}-log-{now}.txt'

        output_file(logout_file_path, log_str)


def zte_configfile_collect(ip_item, dev_list):
    if ip_item[3] == 'telnet':
        dev_list['device_type'] = 'zte_zxros_telnet'
    elif ip_item[3] == 'ssh':
        dev_list['device_type'] = 'zte_zxros'
    c_start_time = time.time()
    print(
        f'{ip_item[0]}:采集开始！时间{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c_start_time))}.')
    try:
        connect = ConnectHandler(**dev_list)
    except NetmikoAuthenticationException:  # 认证失败报错记录
        print(ip_item[0], '认证失败！')
        connect_err = open(rf'.\登录错误日志\{ip_item[0]}_登录错误_{now}.txt', 'a')
        connect_err.write(ip_item[0] + ':认证失败!！\n')
        connect_err.close()
    except NetmikoTimeoutException:  # 登录超时报错记录
        print(ip_item[0], '连接超时！')
        connect_err = open(rf'.\登录错误日志\{ip_item[0]}_登录错误_{now}.txt', 'a')
        connect_err.write(ip_item[0] + ':连接超时！\n')
        connect_err.close()
    except ConnectionRefusedError:  # 拒绝连接报错记录
        print(ip_item[0], '拒绝连接！')
        connect_err = open(rf'.\登录错误日志\{ip_item[0]}_登录错误_{now}.txt', 'a')
        connect_err.write(ip_item[0] + ':拒绝连接！\n')
        connect_err.close()
    else:
        # logging.basicConfig(filename=rf".\操作日志{now}\{ip_item[0]}-log-{now}.txt", level=logging.DEBUG)
        hostname = connect.send_command('show hostname')
        job_col = connect.save_config()
        connect.disconnect()
        c_end_time = time.time()
        print(f'{ip_item[0]}:采集完成！耗时{c_end_time - c_start_time:.3f}秒')
        log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                      ':' + ip_item[1] + ':' + dev_list['port'])

        log_str += '\n##############################\n' + job_col
        logout_file_path = rf'.\操作日志{now}\{hostname}-log-{now}.txt'

        output_file(logout_file_path, log_str)


def configfile_collect(ip_item, dev_list):
    if ip_item[4] == 'huawei':
        huawei_configfile_collect(ip_item, dev_list)
    elif ip_item[4] == 'zte':
        zte_configfile_collect(ip_item, dev_list)


read_file_path = r'设备IP地址.txt'
now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

ip_list = read_file(read_file_path)
dev_info = {
    'device_type': 'huawei_telnet',
    'username': input('设备帐号：'),
    'ip': '',
    'port': '23',
    'password': getpass.getpass('设备密码：')
}
if not os.path.isdir(f'操作日志{now}'):
    os.mkdir(f'操作日志{now}')
if not os.path.isdir(f'登录错误日志{now}'):
    os.mkdir(f'登录错误日志{now}')


dev_info_list = []
for dev_list in ip_list:
    dev_info['ip'] = dev_list[1]
    dev_info['port'] = dev_list[2]
    dev_info_list.append(dev_info.copy())
start = time.time()
with ThreadPoolExecutor(max_workers=10) as do:
    do.map(configfile_collect, ip_list, dev_info_list)

end = time.time()

print(f'共耗时{end - start:.3f}秒配置保存工作完成。')
