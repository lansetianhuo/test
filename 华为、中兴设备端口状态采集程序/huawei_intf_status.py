#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   huawei_intf_status
@时间     :   2021-2-7 14:16
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
import file_func


def data_section(data):
    section = data.split('\n')
    data_list = []
    data_setc_list = []

    for data in section:
        if data != '' and not data.startswith('<') and not data.startswith(
                '[') and not data.startswith('dis'):
            data_setc_list.append(data)
        else:
            data_list.append(data_setc_list)
            data_setc_list = []
    return data_list


def phy_intf_collect(data_list):
    phy_intf_list = []
    for data in data_list:
        if len(data) > 0:
            if data[0].startswith(
                    'GigabitEthernet') or data[0].startswith('100GE'):
                phy_intf_list.append(data)

    return phy_intf_list


def inft_GE_info_collect(intf_data_list, hostname, dev_ip, dev_factory):
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
            phy_state = re.findall(r': ([a-zA-Z]+ ?[a-zA-Z]+)', data_row)[0]

        if data_row.startswith('Line protocol current state'):
            protocol_state = re.findall(
                r'Line protocol current state : (\w+)', data_row)
            if len(protocol_state) > 0:
                protocol_state = protocol_state[0]
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
            if data_row.startswith('Tx Power:'):
                tx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                tx_power = tx_power_list[1].strip(' ')
                tx_range = tx_power_list[-4:-2]
            elif data_row.startswith('Tx Optical Power:'):
                tx_power_list = re.split(r':|,|\[|\]|dBm', data_row)
                tx_power = tx_power_list[1].strip(' ')
                tx_range = tx_power_list[-4:-2]
        else:
            intf_optical = '端口无模块'
            rx_power = 'none'
            tx_power = 'none'
        if data_row.startswith(
                'Input bandwidth utilization') or 'input utility rate' in data_row:
            input_bandwidth = data_row.split(':')[1].strip(' ')
        if data_row.startswith(
                'Output bandwidth utilization') or 'output utility rate' in data_row:
            output_bandwidth = data_row.split(':')[1].strip(' ')
    intf_info_dict['设备名'] = hostname
    intf_info_dict['设备IP'] = dev_ip
    intf_info_dict['端口名'] = intf_name
    intf_info_dict['管理状态'] = phy_state
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
    intf_info_dict['设备厂商'] = dev_factory
    if phy_state == 'Administratively DOWN':
        intf_info_dict['管理状态'] = 'DOWN'
        intf_info_dict['物理状态'] = 'DOWN'
    if intf_info_dict['模块类型'] != 'none':
        if intf_info_dict['模块类型'] == "SingleMode":
            intf_info_dict['模块类型'] = '单模'
        if intf_info_dict['模块类型'] == "single mode":
            intf_info_dict['模块类型'] = '单模'
        if intf_info_dict['模块类型'] == "MultiMode":
            intf_info_dict['模块类型'] = '多模'
        if intf_info_dict['模块类型'] == "Copper Mode":
            intf_info_dict['模块类型'] = '电口'
    if rx_power != 'none':
        if float(rx_range[0]) <= float(rx_power) <= float(rx_range[1]):
            intf_info_dict['收光状态'] = '收光正常'
        elif float(rx_range[0]) >= float(rx_power):
            intf_info_dict['收光状态'] = '收光低'
        elif float(rx_power) >= float(rx_range[1]):
            intf_info_dict['收光状态'] = '收光高'
        else:
            intf_info_dict['收光状态'] = '收光不正常'
    return intf_info_dict


def inft_100GE_info_collect(intf_data_list, hostname, dev_ip, dev_factory):
    intf_name = 'none'
    phy_state = 'DOWN'
    protocol_state = 'DOWN'
    description = 'none'
    port_bw = 'none'
    transceiver_mode = 'none'
    distance = 'none'
    rx_power = []
    rx_range = []
    tx_power = []
    tx_range = []
    input_bandwidth = 'none'
    output_bandwidth = 'none'
    intf_optical = 'none'
    rx_power_str = 'none'
    tx_power_str = 'none'
    intf_info_dict = {}
    for data_row in intf_data_list:
        data_row = data_row.strip(' ')
        if data_row.startswith('100GE'):
            port_list = data_row.split(' ')
            intf_name = port_list[0]
            phy_state = re.findall(r': ([a-zA-Z]+ ?[a-zA-Z]+)', data_row)[0]
        if data_row.startswith('Line protocol current state'):
            protocol_state = re.findall(
                r'Line protocol current state : (\w+)', data_row)
            if len(protocol_state) > 0:
                protocol_state = protocol_state[0]
        if data_row.startswith('Description:'):
            description = data_row.replace('Description:', '')
        # if not data_row.startswith('Optical transceiver is offline'):
        # if data_row != 'Optical transceiver is offline!':
        if 'Optical transceiver is offline' not in data_row:
            # if data_row.startswith('Transceiver max BW:'):
            #     port_bw_list = re.split(r'[:,]', data_row)
            #     port_bw = '100G'
            #     transceiver_mode = port_bw_list[-1].strip(' ')
            if 'Transceiver Mode:' in data_row:
                port_bw_list = re.split(r'Transceiver Mode: ', data_row)
                port_bw = '100G'
                transceiver_mode = port_bw_list[-1].strip(' ')
            if 'Transmission Distance:' in data_row:
                distance = re.split(r'Transmission Distance:',
                                    data_row)[-1].strip(' ')
            if data_row.startswith('Rx warning range: ') or \
                    data_row.startswith('Rx Warning range: '):
                rx_power_list = re.split(r',|\[|\]|dBm',
                                         data_row.replace(' ', ''))
                rx_range = rx_power_list[1:3]
                tx_range = rx_power_list[6:8]
            if data_row.startswith('Rx Power[0]:'):
                rx_power_list = re.split(
                    r':|dBm', data_row.replace(' ', ''))
                rx_power.append(rx_power_list[1])
                tx_power.append(rx_power_list[3])
            if data_row.startswith('Rx Power[1]:'):
                rx_power_list = re.split(
                    r':|dBm', data_row.replace(' ', ''))
                rx_power.append(rx_power_list[1])
                tx_power.append(rx_power_list[3])
            if data_row.startswith('Rx Power[2]:'):
                rx_power_list = re.split(
                    r':|dBm', data_row.replace(' ', ''))
                rx_power.append(rx_power_list[1])
                tx_power.append(rx_power_list[3])
            if data_row.startswith('Rx Power[3]:'):
                rx_power_list = re.split(
                    r':|dBm', data_row.replace(' ', ''))
                rx_power.append(rx_power_list[1])
                tx_power.append(rx_power_list[3])
                rx_power_str = ',\n'.join(rx_power)
                tx_power_str = ',\n'.join(tx_power)

        else:
            intf_optical = '端口无模块'
            rx_power_str = 'none'
            tx_power_str = 'none'

        if data_row.startswith('Input bandwidth utilization') or (
                'input utility rate' in data_row):
            input_bandwidth = data_row.split(':')[1].strip(' ')
        if data_row.startswith('Output bandwidth utilization') or (
                'output utility rate' in data_row):
            output_bandwidth = data_row.split(':')[1].strip(' ')
    intf_info_dict['设备名'] = hostname
    intf_info_dict['设备IP'] = dev_ip
    intf_info_dict['端口名'] = intf_name
    intf_info_dict['管理状态'] = phy_state
    intf_info_dict['物理状态'] = phy_state
    intf_info_dict['协议状态'] = protocol_state
    intf_info_dict['端口描述'] = description
    intf_info_dict['带宽'] = port_bw
    intf_info_dict['模块类型'] = transceiver_mode
    intf_info_dict['模块距离'] = distance
    intf_info_dict['收光'] = rx_power_str
    intf_info_dict['收光范围'] = rx_range[:]
    intf_info_dict['发光'] = tx_power_str
    intf_info_dict['发光范围'] = tx_range[:]
    intf_info_dict['入流量%'] = input_bandwidth
    intf_info_dict['出流量%'] = output_bandwidth
    intf_info_dict['收光状态'] = intf_optical
    intf_info_dict['设备厂商'] = dev_factory
    if phy_state == 'Administratively DOWN':
        intf_info_dict['管理状态'] = 'DOWN'
        intf_info_dict['物理状态'] = 'DOWN'
    if intf_info_dict['模块类型'] != 'none':
        if intf_info_dict['模块类型'] == "SingleMode" or intf_info_dict['模块类型'] \
                == "single mode" or intf_info_dict['模块类型'] == "Single Mode":
            intf_info_dict['模块类型'] = '单模'
        if intf_info_dict['模块类型'] == "MultiMode":
            intf_info_dict['模块类型'] = '多模'

    if intf_info_dict['收光'] != 'none' and intf_optical != '端口无模块':
        rx_power_status = []
        for rx_power_value in rx_power:
            if float(
                    rx_range[0]) <= float(rx_power_value) <= float(
                    rx_range[1]):
                rx_power_status.append('收光正常')
            elif float(rx_range[0]) >= float(rx_power_value):
                rx_power_status.append('收光低')
            elif float(rx_power_value) >= float(rx_range[1]):
                rx_power_status.append('收光高')
            else:
                rx_power_status.append('收光不正常')
        intf_info_dict['收光状态'] = ',\n'.join(rx_power_status)
    return intf_info_dict


def inft_info_collect(phy_intf_list, hostname, dev_ip, dev_factory):
    inft_info_dict_list = []
    for intf_data_list in phy_intf_list:
        if intf_data_list[0].startswith('GigabitEthernet') and (
                not intf_data_list[0].startswith('GigabitEthernet0/0/0')):
            inft_info_dict_list.append(
                inft_GE_info_collect(
                    intf_data_list,
                    hostname,
                    dev_ip,
                    dev_factory))
        elif intf_data_list[0].startswith('100GE'):
            inft_info_dict_list.append(
                inft_100GE_info_collect(
                    intf_data_list,
                    hostname,
                    dev_ip,
                    dev_factory))

    # if inft_info_dict_list[0]['端口名'] == 'GigabitEthernet0/0/0':
    #     del inft_info_dict_list[0]
    return inft_info_dict_list


def inf_status(read_file_path, write_file_path, hostname, dev_ip, dev_factory):
    # read_file_path = r'D:\xuexi\cheshiwenjian\华为端口状态新省ER1.txt'
    # write_file_path = r'D:\xuexi\cheshiwenjian\MSE端口.csv'
    data = file_func.read_file(read_file_path)
    data_list = data_section(data)
    # print(data_list)
    phy_intf_list = phy_intf_collect(data_list)
    # print(phy_intf _list)
    inft_info_dict_list = inft_info_collect(
        phy_intf_list, hostname, dev_ip, dev_factory)
    file_func.write_csv(write_file_path, inft_info_dict_list)
    return inft_info_dict_list
