#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   华为指定端口状态-csv.py
@时间     :   2020-11-29 16:56
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here

import re
import csv


def read_file(file_path):
    with open(file_path, 'r', encoding='UTF-8-sig') as file:
        data = file.read()
        data.strip('\n')
    return data


def data_section(data):
    section = data.split('\n')
    data_list = []
    data_setc_list = []
    for data in section:
        if data != '':
            data_setc_list.append(data)
        else:
            data_list.append(data_setc_list)
            data_setc_list = []
    return data_list


def phy_intf_collect(data_list):
    phy_intf_list = []
    for data in data_list:
        if data[1].startswith('GigabitEthernet'):
            phy_intf_list.append(data)
    return phy_intf_list


def inft_info_collect(phy_intf_list):
    inft_info_dict_list = []
    for intf_data_list in phy_intf_list:
        intf_name = 'none'
        phy_state = 'DOWN'
        protocol_state = 'DOWN'
        description = 'none'
        port_bw = 'none'
        transceiver_mode = 'none'
        distance = 'none'
        rx_power = 'none'
        rx_range = []
        tx_power = 'none'
        tx_range = []
        input_bandwidth = 'none'
        output_bandwidth = 'none'
        intf_optical = 'none'

        intf_info_dict = {}
        for data_row in intf_data_list:
            data_row = data_row.strip(' ')
            if data_row.startswith('GigabitEthernet'):
                port_list = data_row.split(' ')
                intf_name = port_list[0]
                phy_state = port_list[-1]
            if data_row.startswith('Line protocol current state'):
                protocol_state = re.findall(
                    r'Line protocol current state : (\w+)', data_row)
            if data_row.startswith('Description:'):
                description = data_row.replace('Description:', '')
            if not data_row.startswith('Optical transceiver is offline'):
                if data_row.startswith('Port BW:'):
                    port_bw_list = re.split(r'[:,]', data_row)
                    port_bw = port_bw_list[1].strip(' ')
                    transceiver_mode = port_bw_list[-1].strip(' ')
                if data_row.startswith('WaveLength:'):
                    distance = re.split(r'[:,]', data_row)[-1].strip(' ')
                if data_row.startswith('Rx Power:'):
                    rx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                    rx_power = rx_power_list[1].strip(' ')
                    rx_range = rx_power_list[-4:-2]
                elif data_row.startswith('Rx Optical Power:'):
                    rx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                    rx_power = rx_power_list[1].strip(' ')
                    rx_range = rx_power_list[-4:-2]
                if data_row.startswith('Rx Power:'):
                    tx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                    tx_power = tx_power_list[1].strip(' ')
                    tx_range = tx_power_list[-4:-2]
                elif data_row.startswith('Tx Optical Power:'):
                    tx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                    tx_power = tx_power_list[1].strip(' ')
                    tx_range = tx_power_list[-4:-2]
            else:
                intf_optical = '端口无模块'
            if data_row.startswith('Input bandwidth utilization'):
                input_bandwidth = data_row.split(':')[1].strip(' ')
            if data_row.startswith('Output bandwidth utilization'):
                output_bandwidth = data_row.split(':')[1].strip(' ')

        intf_info_dict['端口名'] = intf_name
        intf_info_dict['物理状态'] = phy_state
        intf_info_dict['协议状态'] = protocol_state
        intf_info_dict['端口描述'] = description
        intf_info_dict['带宽'] = port_bw
        intf_info_dict['模块类型'] = transceiver_mode
        intf_info_dict['模块距离'] = distance
        intf_info_dict['收光'] = rx_power
        intf_info_dict['收光范围'] = rx_range[:]
        intf_info_dict['发光'] = tx_power
        intf_info_dict['发光范围'] = tx_range[:]
        intf_info_dict['入流量%'] = input_bandwidth
        intf_info_dict['出流量%'] = output_bandwidth
        intf_info_dict['收光状态'] = intf_optical
        if intf_info_dict['模块类型'] != 'none':
            if intf_info_dict['模块类型'] == "SingleMode":
                intf_info_dict['模块类型'] = '单模'
            if intf_info_dict['模块类型'] == "MultiMode":
                intf_info_dict['模块类型'] = '多模'
            if intf_info_dict['模块类型'] == "Copper Mode":
                intf_info_dict['模块类型'] = '电口'
        if intf_info_dict['收光'] != 'none':
            if float(rx_range[0]) <= float(rx_power) <= float(rx_range[1]):
                intf_info_dict['收光状态'] = '收光正常'
            elif float(rx_range[0]) >= float(rx_power):
                intf_info_dict['收光状态'] = '收光低'
            elif float(rx_power) >= float(rx_range[1]):
                intf_info_dict['收光状态'] = '收光高'
            else:
                intf_info_dict['收光状态'] = '收光不正常'

        inft_info_dict_list.append(intf_info_dict)
    if inft_info_dict_list[0]['端口名'] == 'GigabitEthernet0/0/0':
        del inft_info_dict_list[0]
    return inft_info_dict_list


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def main():
    read_file_path = r'D:\xuexi\cheshiwenjian\华为端口状态新省ER1.txt'
    write_file_path = r'D:\xuexi\cheshiwenjian\EPC CE1端口.csv'
    data = read_file(read_file_path)
    data_list = data_section(data)
    phy_intf_list = phy_intf_collect(data_list)
    inft_info_dict_list = inft_info_collect(phy_intf_list)
    write_csv(write_file_path, inft_info_dict_list)


if __name__ == '__main__':
    main()
