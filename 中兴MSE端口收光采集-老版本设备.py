#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   中兴MSE端口收光采集-老版本设备
@时间     :   2021-2-9 15:12
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
            bw = 'none'
            rx_power = 'none'
            tx_power = 'none'
            flow_in = '0'
            flow_out = '0'
            name_list = re.split(r'-', data_row[0])
            if name_list[0] == 'gei':
                bw = '1G'
            elif name_list[0] == 'xgei':
                bw = '10G'
            elif name_list[0] == 'cgei':
                bw = '100G'

            intf_info_dict = {}
            intf_info_dict['端口名'] = data_row[0]
            intf_info_dict['带宽'] = bw
            intf_info_dict['收光'] = data_row[6]
            intf_info_dict['发光'] = data_row[6]
            intf_info_dict['入流量'] = data_row[2] + '%'
            intf_info_dict['出流量'] = data_row[4] + '%'

            if 'N/A' in rx_power:
                intf_info_dict['收光状态'] = '无收光'
            inft_info_dict_list.append(intf_info_dict)

    return inft_info_dict_list


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def main():
    read_file_path = r'D:\xuexi\cheshiwenjian\中兴MSE端口收光-老.txt'
    write_file_path = r'D:\xuexi\cheshiwenjian\中兴MSE端口类型-老.csv'
    data_str = read_file(read_file_path)
    data_list = data_section(data_str)
    inft_info_dict_list = inft_info_collect(data_list)
    write_csv(write_file_path, inft_info_dict_list)


if __name__ == '__main__':
    main()
