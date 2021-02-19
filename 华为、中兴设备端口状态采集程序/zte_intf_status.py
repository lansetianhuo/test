#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   zte_intf_status_new
@时间     :   2021-2-15 12:58
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
import file_func


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


def inft_power_collect_v3(phy_intf_power_list, hostname, dev_ip, dev_factory):
    inft_power_dict_list = []
    for power_data_row in phy_intf_power_list:
        # intf_name_keywords=['gei','xgei','cgei']
        # if any(name_keyword in data_row[0] for name_keyword in
        # intf_name_keywords):
        if 'gei' in power_data_row[0]:
            # if data_row[0].find('gei') != -1:
            # intf_name = 'none'
            transceiver_mode = 'none'
            port_bw = 'none'
            distance = 'none'
            rx_power = 'none'
            rx_low = 'none'
            rx_high = 'none'
            tx_power = 'none'
            # intf_optical = 'none'
            intf_power_dict = {}
            intf_power_dict['设备名'] = hostname
            intf_power_dict['设备IP'] = dev_ip
            intf_optical = power_data_row[1]
            intf_power_dict['端口名'] = power_data_row[0]
            if intf_optical != 'offline':
                # intf_name = data_row[0]
                intf_optical_list = re.split(r'-', intf_optical)
                port_bw = intf_optical_list[0]
                distance = intf_optical_list[1]
                transceiver_mode = power_data_row[2].strip('nm')

                rx_power_list = re.split(
                    r'[\[,\]]', power_data_row[3].replace(
                        '/', ''))
                rx_power = rx_power_list[0]
                rx_low = rx_power_list[1]
                rx_high = rx_power_list[2]
                tx_power_list = re.split(
                    r'[\[,\]]', power_data_row[4].replace(
                        '/', ''))
                tx_power = tx_power_list[0]
                tx_low = tx_power_list[1]
                tx_high = tx_power_list[2]

                # intf_info_dict['端口名'] = intf_name
                intf_power_dict['管理状态'] = 'none'
                intf_power_dict['物理状态'] = 'none'
                intf_power_dict['协议状态'] = 'none'
                intf_power_dict['端口描述'] = 'none'
                intf_power_dict['带宽'] = port_bw
                intf_power_dict['模块类型'] = transceiver_mode
                intf_power_dict['模块距离'] = distance
                intf_power_dict['收光'] = rx_power
                intf_power_dict['收光范围'] = [rx_low, rx_high]
                intf_power_dict['发光'] = tx_power
                intf_power_dict['发光范围'] = [tx_low, tx_high]
                intf_power_dict['入流量%'] = 'none'
                intf_power_dict['出流量%'] = 'none'
                intf_power_dict['收光状态'] = intf_optical
                intf_power_dict['设备厂商'] = dev_factory
            if intf_optical == 'offline':
                intf_power_dict['收光状态'] = '端口无模块'
                intf_power_dict['模块类型'] = transceiver_mode
                intf_power_dict['带宽'] = port_bw
                intf_power_dict['模块距离'] = distance
                intf_power_dict['收光'] = rx_power
                intf_power_dict['收光范围'] = [rx_low, rx_high]
                intf_power_dict['发光'] = tx_power
                intf_power_dict['收光状态'] = intf_optical
            else:
                # rx_low_info=['N','A','none']
                # if any(data_str in rx_low for data_str in rx_low_info):
                if 'N' in rx_low or 'none' in rx_low:
                    intf_power_dict['收光状态'] = '收光范围不正常'
                elif 'N' in rx_power:
                    intf_power_dict['收光状态'] = '无收光'
                elif float(rx_low) <= float(rx_power) <= float(rx_high):
                    intf_power_dict['收光状态'] = '收光正常'
                elif float(rx_low) >= float(rx_power):
                    intf_power_dict['收光状态'] = '收光低'
                elif float(rx_power) >= float(rx_high):
                    intf_power_dict['收光状态'] = '收光高'
                else:
                    intf_power_dict['收光状态'] = '收光不正常'
                if int(intf_power_dict['模块类型']) > 850:
                    intf_power_dict['模块类型'] = '单模'
                else:
                    intf_power_dict['模块类型'] = '多模'
                if not port_bw.endswith('G'):
                    intf_power_dict['带宽'] = str(int(port_bw) / 1000) + 'G'
            inft_power_dict_list.append(intf_power_dict)
    return inft_power_dict_list


def inft_flow_collect(phy_intf_flow_list):
    inft_flow_dict_list = []
    for flow_data_row in phy_intf_flow_list:
        # intf_name_keywords=['gei','xgei','cgei']
        # if any(name_keyword in data_row[0] for name_keyword in
        # intf_name_keywords):
        if 'gei' in flow_data_row[0]:
            # if data_row[0].find('gei') != -1:
            intf_name = 'none'
            flow_in = '0'
            flow_out = '0'
            name_list = re.split(r'-', flow_data_row[0])
            if name_list[0] == 'gei':
                port_bw = '1G'
            elif name_list[0] == 'xgei':
                port_bw = '10G'
            elif name_list[0] == 'cgei':
                port_bw = '100G'

            intf_flow_dict = {}
            intf_flow_dict['端口名'] = flow_data_row[0]
            intf_flow_dict['带宽'] = port_bw
            intf_flow_dict['入流量%'] = flow_data_row[1] + '%'
            intf_flow_dict['出流量%'] = flow_data_row[2] + '%'
            intf_flow_dict['端口描述'] = 'none'
            if len(flow_data_row) > 4:
                intf_flow_dict['端口描述'] = ''.join(flow_data_row[4:])
            inft_flow_dict_list.append(intf_flow_dict)

    return inft_flow_dict_list


def inft_status_collectv3(phy_intf_status_list):
    inft_status_dict_list = []
    for status_data_row in phy_intf_status_list:
        # intf_name_keywords=['gei','xgei','cgei']
        # if any(name_keyword in data_row[0] for name_keyword in
        # intf_name_keywords):
        if 'gei' in status_data_row[0]:
            # if data_row[0].find('gei') != -1:
            intf_name = 'none'
            admin_status = 'down'
            phy_status = 'down'
            intf_bw = '0'
            intf_status_dict = {}

            intf_status_dict['端口名'] = status_data_row[0]
            intf_status_dict['管理状态'] = status_data_row[4]
            intf_status_dict['物理状态'] = status_data_row[5]
            intf_status_dict['协议状态'] = status_data_row[6]
            intf_status_dict['带宽'] = str(int(status_data_row[3]) // 1000) + 'G'
            inft_status_dict_list.append(intf_status_dict)
    return inft_status_dict_list


def zte_inf_status_v3(
        optical_file_path,
        flow_file_path,
        intf_desc_file_path,
        write_csv_path, hostname, dev_ip, dev_factory):

    power_data_str = file_func.read_file(optical_file_path)
    power_data_list = data_section(power_data_str)
    inft_power_dict_list = inft_power_collect_v3(
        power_data_list, hostname, dev_ip, dev_factory)

    flow_data_str = file_func.read_file(flow_file_path)
    flow_data_list = data_section(flow_data_str)
    inft_flow_dict_list = inft_flow_collect(flow_data_list)

    status_data_str = file_func.read_file(intf_desc_file_path)
    status_data_list = data_section(status_data_str)
    inft_status_dict_list = inft_status_collectv3(status_data_list)

    for intf_power_list in inft_power_dict_list:
        intf_power_list['管理状态'] = 'none'
        intf_power_list['物理状态'] = 'none'
        intf_power_list['协议状态'] = 'none'
        for intf_flow_list in inft_flow_dict_list:
            if intf_power_list['端口名'] == intf_flow_list['端口名']:
                intf_power_list['入流量%'] = intf_flow_list['入流量%']
                intf_power_list['出流量%'] = intf_flow_list['出流量%']
                intf_power_list['端口描述'] = intf_flow_list['端口描述']
                break

        for intf_status_list in inft_status_dict_list:
            if intf_power_list['端口名'] == intf_status_list['端口名']:
                intf_power_list['管理状态'] = intf_status_list['管理状态']
                intf_power_list['物理状态'] = intf_status_list['物理状态']
                intf_power_list['协议状态'] = intf_status_list['协议状态']
                intf_power_list['带宽'] = intf_status_list['带宽']
                break

    file_func.write_csv(write_csv_path, inft_power_dict_list)
    return inft_power_dict_list


def inft_power_collect_v2(phy_intf_list, hostname, dev_ip, dev_factory):
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
            intf_info_dict['设备名'] = hostname
            intf_info_dict['设备IP'] = dev_ip
            intf_info_dict['端口名'] = data_row[0]
            intf_info_dict['管理状态'] = 'none'
            intf_info_dict['物理状态'] = 'none'
            intf_info_dict['协议状态'] = 'none'
            intf_info_dict['端口描述'] = 'none'
            intf_info_dict['带宽'] = bw
            intf_info_dict['模块类型'] = 'none'
            intf_info_dict['模块距离'] = 'none'
            intf_info_dict['收光'] = data_row[6]
            intf_info_dict['收光范围'] = 'none'
            intf_info_dict['发光'] = data_row[7]
            intf_info_dict['发光范围'] = 'none'
            intf_info_dict['入流量%'] = data_row[2] + '%'
            intf_info_dict['出流量%'] = data_row[4] + '%'
            intf_info_dict['收光状态'] = 'none'
            intf_info_dict['设备厂商'] = dev_factory

            if 'N/A' in rx_power:
                intf_info_dict['收光状态'] = '无收光'
            inft_info_dict_list.append(intf_info_dict)
    return inft_info_dict_list


def inft_status_collectv2(phy_intf_status_list):
    inft_status_dict_list = []
    for status_data_row in phy_intf_status_list:
        # intf_name_keywords=['gei','xgei','cgei']
        # if any(name_keyword in data_row[0] for name_keyword in
        # intf_name_keywords):
        if 'gei' in status_data_row[0]:
            # if data_row[0].find('gei') != -1:
            intf_name = 'none'
            admin_status = 'down'
            phy_status = 'down'
            intf_bw = '0'
            intf_status_dict = {}

            intf_status_dict['端口名'] = status_data_row[0]
            intf_status_dict['管理状态'] = status_data_row[1]
            intf_status_dict['物理状态'] = status_data_row[2]
            intf_status_dict['协议状态'] = status_data_row[3]
            intf_status_dict['端口描述'] = status_data_row[4]
            inft_status_dict_list.append(intf_status_dict)
    return inft_status_dict_list


def zte_inf_status_v2(
        optical_file_path,intf_desc_file_path,write_csv_path,hostname,dev_ip,dev_factory):

    power_data_str = file_func.read_file(optical_file_path)
    power_data_list = data_section(power_data_str)
    inft_power_dict_list = inft_power_collect_v2(power_data_list, hostname, dev_ip, dev_factory)
    status_data_str = file_func.read_file(intf_desc_file_path)
    status_data_list = data_section(status_data_str)
    inft_status_dict_list = inft_status_collectv2(status_data_list)

    for intf_power_list in inft_power_dict_list:
        intf_power_list['管理状态'] = 'none'
        intf_power_list['物理状态'] = 'none'
        intf_power_list['协议状态'] = 'none'

        for intf_status_list in inft_status_dict_list:
            if intf_power_list['端口名'] == intf_status_list['端口名']:
                intf_power_list['管理状态'] = intf_status_list['管理状态']
                intf_power_list['物理状态'] = intf_status_list['物理状态']
                intf_power_list['协议状态'] = intf_status_list['协议状态']
                intf_power_list['端口描述'] = intf_status_list['端口描述']
                break
    file_func.write_csv(write_csv_path, inft_power_dict_list)
    return inft_power_dict_list
