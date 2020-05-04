#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   华为端口状态.py
@时间     :   2020-5-4 15:20
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
import xlwings as xw

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
        if data[0].startswith('GigabitEthernet'):
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
        rx_range = 'none'
        tx_power = 'none'
        tx_range = 'none'
        input_bandwidth = 'none'
        output_bandwidth = 'none'

        intf_info_dict = {}
        for data_row in intf_data_list:
            data_row = data_row.strip(' ')
            if data_row.startswith('GigabitEthernet'):
                port_list = data_row.split(' ')
                intf_name = port_list[0]
                phy_state = port_list[-1]
            if data_row.startswith('Line protocol current state'):
                user_vlan_data = re.findall(
                    r'Line protocol current state : (\w+)', data_row)
            if data_row.startswith('Description:'):
                description = data_row.replace('Description:', '')
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
            if data_row.startswith('Rx Power:'):
                tx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                tx_power = tx_power_list[1].strip(' ')
                tx_range = tx_power_list[-4:-2]
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
        intf_info_dict['收光范围'] = str(rx_range)
        intf_info_dict['发光'] = tx_power
        intf_info_dict['发光范围'] = str(tx_range)
        intf_info_dict['入流量%'] = input_bandwidth
        intf_info_dict['出流量%'] = output_bandwidth
        intf_info_dict['收光状态'] = '无模块'
        if intf_info_dict['模块类型'] != 'none':
            if intf_info_dict['模块类型'] == "SingleMode":
                intf_info_dict['模块类型'] = '单模'
        if rx_power != 'none':
            if float(rx_range[0]) <= float(rx_power) <= float(rx_range[1]):
                intf_info_dict['收光状态'] = '收光正常'
            elif float(rx_range[0]) >= float(rx_power):
                intf_info_dict['收光状态'] = '收光低'
            elif float(rx_power) >= float(rx_range[0]):
                intf_info_dict['收光状态'] = '收光高'
            else:
                intf_info_dict['收光状态'] = '收光不正常'

        inft_info_dict_list.append(intf_info_dict)
    return inft_info_dict_list

def write_excel(write_file_path,list_data):
    # print(list)
    data_list = []
    data_list.append(list(list_data[0]))
    for data in list_data:
        data_list.append(list(data.values()))
    # print(data_list)

    app = xw.App(visible=False, add_book=False)
    wb = app.books.add()
    wb.sheets.add("端口状态")
    sht = wb.sheets["端口状态"]
    sht.range('A1').expand('table').value = data_list
    wb.save(write_file_path)
    wb.close()
    app.quit()


def main():
    read_file_path = r'D:\xuexi\cheshiwenjian\华为端口状态.txt'
    write_file_path = r'D:\xuexi\cheshiwenjian\华为端口状态.xlsx'
    data = read_file(read_file_path)
    data_list = data_section(data)
    phy_intf_list = phy_intf_collect(data_list)
    inft_info_dict_list = inft_info_collect(phy_intf_list)
    write_excel(write_file_path, inft_info_dict_list)


if __name__ == '__main__':
    main()
