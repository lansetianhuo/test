#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@文件     :   华为lldp邻居信息.py
@时间     :   2020/03/10 09:39:45
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
'''
# Start typing your code from here

import re

lldp_path = r"D:\xuexi\cheshiwenjian\lldp.txt"

with open(lldp_path, 'r', encoding='utf-8-sig') as file_lldp:
    lldp_data = file_lldp.read()

lldp_data = lldp_data.strip(' ')

lldp_data_list = re.split('\n', lldp_data)

lldp_sub = []
lldp_sub_set = []
for lldp_data_row in lldp_data_list:
    lldp_data_row = lldp_data_row.strip(' ')
    if lldp_data_row != '':
        lldp_sub.append(lldp_data_row)
    else:
        if len(lldp_sub):
            lldp_sub_set.append(lldp_sub)
            lldp_sub = []
# lldp_intf_sub = []
# intf_data = ""
# for lldp_intf in lldp_sub_set:
#     if len(lldp_intf) > 1:
#         intf_port = re.split(r' ', lldp_intf[0])[0]
#         intf_remote_dev = re.findall(r'SysName: (.+)', lldp_intf[7])
#         intf_remote_port = re.findall(r'PortId: (.+)', lldp_intf[5])
#         intf_data = intf_data + str(intf_port) + " " + ''.join(
#             intf_remote_dev) + " " + ''.join(intf_remote_port) + "\n"
#     else:
#         intf_port = re.split(r' ', lldp_intf[0])[0]
#         intf_data = intf_data + str(intf_port) + "\n"

inft_data_set = ""
for intf_data in lldp_sub_set:
    remote_dev = "none"
    remote_port = "none"
    for intf_data_sub in intf_data:
        if intf_data_sub.endswith('neighbor:'):
            intf_port = re.split(r' ', intf_data_sub)[0]
        elif intf_data_sub.startswith('SysName:'):
            remote_dev = intf_data_sub.replace('SysName:', '').strip(' ')
        elif intf_data_sub.startswith('PortId:'):
            remote_port = intf_data_sub.replace('PortId:', '').strip(' ')
        else:
            pass
    inft_data_set = inft_data_set + str(
        intf_port) + " " + remote_dev + " " + remote_port + "\n"

lldp_fin_path = r"D:\xuexi\cheshiwenjian\lldp_fin.txt"

with open(lldp_fin_path, 'w') as file_fin_lldp:
    file_fin_lldp.write(inft_data_set)
