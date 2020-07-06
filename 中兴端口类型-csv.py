#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   中兴端口类型-csv.py
@时间     :   2020-5-13 15:04
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
    section = data.split('HL-QQ-FQ-MSE-1.MAN.M6000#')
    data_list = []
    for data in section:
        if data != '':
            data_list.append(data)
    return data_list


def inft_info_collect(phy_intf_list):
    inft_info_dict_list = []
    for data_row in phy_intf_list:
        intf_name = 'none'
        transceiver_mode = 'none'
        bw = 'none'
        distance = 'none'
        rx_power = 'none'
        rx_low = 'none'
        rx_high = 'none'
        tx_power = 'none'
        intf_optical = 'none'

        intf_info_dict = {}
        intf_optical = re.findall(r'The optical module is (.+)\n', data_row)[0]
        if intf_optical != 'offline':
            intf_name = re.findall(r'^show opticalinfo (.+)\n', data_row)[0]
            print(intf_name)
            intf_optical = re.findall(r'The optical module is (.+)\n', data_row)[0]
            bw = re.findall(r'Ethernet Compliance Codes: (\S+)B', data_row)[0]
            transceiver_mode = re.findall(r'Laser Wavelength: (\S+)', data_row)[0]
            distance = re.findall(r'Transfer Distance:9/125\(Smf\) um fiber ('
                                  r'\S+)', data_row)[0]
            rx_power = re.findall(r'Measured RX Input  Power: (\S+)', data_row)[0]
            tx_power = re.findall(r'Measured TX Output Power: (\S+)', data_row)[0]
            rx_low = re.findall(r'Receiver Sensitivity    : (\S+)', data_row)[0]
            rx_high = re.findall(r'Receiver Overload       : (\S+)', data_row)[0]

            intf_info_dict['端口名'] = intf_name
            intf_info_dict['模块类型'] = transceiver_mode
            intf_info_dict['带宽'] = bw
            intf_info_dict['模块距离'] = str(int(distance) / 1000) + 'KM'
            intf_info_dict['收光'] = rx_power
            intf_info_dict['收光范围'] = [rx_low, rx_high]
            intf_info_dict['发光'] = tx_power
            intf_info_dict['收光状态'] = intf_optical

        if intf_optical == 'offline':
            intf_info_dict['收光状态'] = '端口无模块'
        else:
            if rx_power != 'none' and rx_power != 'N/A':
                if float(rx_low) <= float(rx_power) <= float(rx_high):
                    intf_info_dict['收光状态'] = '收光正常'
                elif float(rx_low) >= float(rx_power):
                    intf_info_dict['收光状态'] = '收光低'
                elif float(rx_power) >= float(rx_high):
                    intf_info_dict['收光状态'] = '收光高'
            else:
                intf_info_dict['收光状态'] = '收光不正常'
            if int(intf_info_dict['模块类型']) > 850:
                intf_info_dict['模块类型'] = '单模'
            else:
                intf_info_dict['模块类型'] = '多模'
            if not bw.endswith('G'):
                intf_info_dict['带宽'] = str(int(bw)/1000)+'G'
        inft_info_dict_list.append(intf_info_dict)

    return inft_info_dict_list


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def main():
    read_file_path = r'D:\xuexi\cheshiwenjian\富区端口信息.txt'
    write_file_path = r'D:\xuexi\cheshiwenjian\中兴端口类型0525.csv'
    data = read_file(read_file_path)
    data_list = data_section(data)
    inft_info_dict_list = inft_info_collect(data_list)
    write_csv(write_file_path, inft_info_dict_list)


if __name__ == '__main__':
    main()
