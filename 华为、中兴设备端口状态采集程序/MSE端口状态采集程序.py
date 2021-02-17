#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   网络设备端口状态采集程序
@时间     :   2021-2-16 4:50
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import time
import os
from netmiko import ConnectHandler
import re
import getpass
import huawei_intf_status
import zte_intf_status
from concurrent.futures import ThreadPoolExecutor


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


def huawei_collect_analysis(ip_item, dev_list):
    dev_list['device_type'] = 'huawei_telnet'

    c_start_time = time.time()
    print(
        f'{ip_item[0]}:采集开始！时间{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c_start_time))}秒')
    connect = ConnectHandler(**dev_list)
    hostname = connect.send_command('display current-configuration | include sysname')[8:]
    info_col_log = connect.send_command('dis int main', strip_prompt=False,
                                        strip_command=False)
    connect.disconnect()
    c_end_time = time.time()
    print(f'{ip_item[0]}:采集完成！耗时{c_end_time - c_start_time:.3f}秒')
    log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                  ':' + ip_item[1] + ':' + dev_list['port'])
    log_str += '\n##############################\n' + info_col_log
    logout_file_path = rf'.\采集日志\{hostname}-log-{now}.txt'

    output_file(logout_file_path, log_str)

    write_csv_path = rf'.\采集结果\{hostname}-{now}.csv'

    huawei_intf_status.inf_status(logout_file_path, write_csv_path)
    end_time = time.time()
    print(f'{ip_item[0]}:提取完成！耗时{end_time - c_end_time:.3f}秒')


def zte_collect_analysis(ip_item, dev_list):
    dev_list['device_type'] = 'zte_zxros_telnet'
    c_start_time = time.time()
    print(
        f'{ip_item[0]}:采集开始！时间{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c_start_time))}秒')
    connect = ConnectHandler(**dev_list)
    version_log = connect.send_command(
        'show version',
        strip_prompt=False,
        strip_command=False).splitlines()[2]
    hostname_log = connect.send_command('show hostname')

    version_id = re.findall(r'.\((\d+.\d+).', version_log)[0]
    if float(version_id) < 3.0:
        optical_info_log = connect.send_command(
            'show intf-statistics utilization phy-interface-only',
            strip_prompt=False,
            strip_command=False)
        connect.disconnect()
        c_end_time = time.time()
        print(f'{ip_item[0]}:采集完成！耗时{c_end_time - c_start_time:.3f}秒')
        log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                      ':' + ip_item[1] + ':' + dev_list['port'])

        log_str += '\n##############################\n' + optical_info_log

        optical_file_path = rf'.\采集日志\{hostname_log}-optical-log-{now}.txt'
        output_file(optical_file_path, log_str)

        write_csv_path = rf'.\采集结果\{hostname_log}-{now}.csv'

        zte_intf_status.zte_inf_status_v2(optical_file_path, write_csv_path)
        end_time = time.time()
        print(f'{ip_item[0]}:提取完成！耗时{end_time - c_end_time:.3f}秒')

    else:
        optical_info_log = connect.send_command(
            'show opticalinfo brief',
            strip_prompt=False,
            strip_command=False)
        flow_info_log = connect.send_command(
            'show intf-statistics utilization phy-interface-only',
            strip_prompt=False,
            strip_command=False)
        intf_desc_info_log = connect.send_command(
            'show interface brief',
            strip_prompt=False,
            strip_command=False)
        connect.disconnect()
        c_end_time = time.time()
        print(f'{ip_item[0]}:采集完成！耗时{c_end_time - c_start_time:.3f}秒')
        log_str = str(log_time + 'Successfully connected to ' + ip_item[0] +
                      ':' + ip_item[1] + ':' + dev_list['port'])
        optical_log_str = log_str
        flow_log_str = log_str
        intf_desc_log_str = log_str
        optical_log_str += '\n##############################\n' + optical_info_log
        flow_log_str += '\n##############################\n' + flow_info_log
        intf_desc_log_str += '\n##############################\n' + intf_desc_info_log
        optical_file_path = rf'.\采集日志\{hostname_log}-optical-log-{now}.txt'
        output_file(optical_file_path, optical_log_str)
        flow_file_path = rf'.\采集日志\{hostname_log}-flow-log-{now}.txt'
        output_file(flow_file_path, flow_log_str)
        intf_desc_file_path = rf'.\采集日志\{hostname_log}-intf-desc-log-{now}.txt'
        output_file(intf_desc_file_path, intf_desc_log_str)

        write_csv_path = rf'.\采集结果\{hostname_log}-{now}.csv'

        zte_intf_status.zte_inf_status_v3(
            optical_file_path,
            flow_file_path,
            intf_desc_file_path,
            write_csv_path)
        end_time = time.time()
        print(f'{ip_item[0]}:提取完成！耗时{end_time - c_end_time:.3f}秒')


def collect_analysis(ip_item, dev_list):
    if ip_item[3] == 'huawei':
        huawei_collect_analysis(ip_item, dev_list)
    elif ip_item[3] == 'zte':
        zte_collect_analysis(ip_item, dev_list,)


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
if not os.path.isdir('采集结果'):
    os.mkdir('采集结果')
if not os.path.isdir('采集日志'):
    os.mkdir('采集日志')
dev_info_list = []
for dev_list in ip_list:
    dev_info['ip'] = dev_list[1]
    dev_info['port'] = dev_list[2]
    dev_info_list.append(dev_info.copy())
start = time.time()
with ThreadPoolExecutor(max_workers=10) as do:
    do.map(collect_analysis, ip_list, dev_info_list)
end = time.time()

print(f'共耗时{end - start:.3f}秒采集提取工作完成。')
