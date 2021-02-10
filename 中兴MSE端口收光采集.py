#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   中兴MSE端口收光采信
@时间     :   2021-2-9 13:17
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
        data_str = file.read()
        data_str = data_str.strip(' ')
        data_str = data_str.strip('\n')
    return data_str


def data_section(data_str):
    data_list = re.split('\n', data_str)
    col_data_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        row_data = row_data.strip('\t')
        row_data = row_data.replace('\t', ' ')
        for col_data in range(row_data.find('  ')):
            row_data = row_data.replace('  ', ' ')
        row_data = re.split(r' ', row_data)
        col_data_list.append(row_data)
    return col_data_list


def inft_info_collect(phy_intf_list):
    inft_info_dict_list = []
    for data_row in phy_intf_list:
        # intf_name_keywords=['gei','xgei','cgei']
        # if any(name_keyword in data_row[0] for name_keyword in
        # intf_name_keywords):
        if 'gei' in data_row[0]:
            # if data_row[0].find('gei') != -1:
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
            intf_optical = data_row[1]
            intf_info_dict['端口名'] = data_row[0]
            if intf_optical != 'offline':
                # intf_name = data_row[0]
                intf_optical_list = re.split(r'-', intf_optical)
                bw = intf_optical_list[0]
                distance = intf_optical_list[1]
                transceiver_mode = data_row[2].strip('nm')

                rx_power_list = re.split(r'[\[,\]]', data_row[3].replace('/',''))
                rx_power = rx_power_list[0]
                rx_low = rx_power_list[1]
                rx_high = rx_power_list[2]
                tx_power_list = re.split(r'[\[,\]]', data_row[4].replace('/',''))
                tx_power = tx_power_list[0]
                tx_low = tx_power_list[1]
                tx_high = tx_power_list[2]

                # intf_info_dict['端口名'] = intf_name
                intf_info_dict['模块类型'] = transceiver_mode
                intf_info_dict['带宽'] = bw
                intf_info_dict['模块距离'] = distance
                intf_info_dict['收光'] = rx_power
                intf_info_dict['收光范围'] = [rx_low, rx_high]
                intf_info_dict['发光'] = tx_power
                intf_info_dict['收光状态'] = intf_optical

            if intf_optical == 'offline':
                intf_info_dict['收光状态'] = '端口无模块'
            else:
                # rx_low_info=['N','A','none']
                # if any(data_str in rx_low for data_str in rx_low_info):
                if 'N' in rx_low or 'none' in rx_low:
                    intf_info_dict['收光状态'] = '收光范围不正常'
                elif 'N' in rx_power:
                    intf_info_dict['收光状态'] = '无收光'
                elif float(rx_low) <= float(rx_power) <= float(rx_high):
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
                    intf_info_dict['带宽'] = str(int(bw) / 1000) + 'G'
            inft_info_dict_list.append(intf_info_dict)

    return inft_info_dict_list


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def main():
    read_file_path = r'D:\xuexi\cheshiwenjian\中兴MSE端口收光.txt'
    write_file_path = r'D:\xuexi\cheshiwenjian\中兴MSE端口类型0603.csv'
    data_str = read_file(read_file_path)
    data_list = data_section(data_str)
    inft_info_dict_list = inft_info_collect(data_list)
    write_csv(write_file_path, inft_info_dict_list)


if __name__ == '__main__':
    main()
