#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   端口数据参数提取
@时间     :   2020-3-24 11:46
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re
import shelve
import csv


def read_data(data_file, data_name):
    data = shelve.open(data_file)
    original_data = data[data_name]
    data.close()
    return original_data


def write_data(file_name, data_name, data):
    stud_db = shelve.open(file_name)
    stud_db[data_name] = data
    stud_db.close()


def write_csv(file_name, list):
    headers = list[0].keys()
    with open(file_name, 'w', encoding='utf-8-sig', newline='') as file:
        file_dict = csv.DictWriter(file, headers)
        file_dict.writeheader()
        file_dict.writerows(list)


def inft_data_collect(intf_data_set):
    inft_data_dict_list = []
    for intf_data_list in intf_data_set:
        intf_name = 'none'
        vlan_list = []
        domain_name = 'none'
        description = 'none'
        ip_address_list = []
        ipv6_address_list = []
        qos_profile_in = 'none'
        qos_profile_out = 'none'
        shutdown = 'none'
        vpn_name = 'none'
        traffic_policy = 'none'
        pw = 'none'
        vpls_name = 'none'
        mtu = 'none'
        isis_router = 'none'
        isis_v6_router = 'none'
        isis_type = 'none'
        isis_level = 'none'
        isis_v6_cost = 'none'
        isis_cost = 'none'
        isis_small_hello = 'none'
        eth_trunk_id = 'none'

        intf_data_dict = {}
        for data_row in intf_data_list:
            data_row = data_row.strip(' ')
            if data_row.startswith('interface'):
                intf_name = data_row.replace('interface ', '')
            if data_row.startswith('user-vlan'):
                user_vlan_data = re.findall(r'user-vlan (\d+\s?\d*)(?: ?qinq )?(\d*\s?\d*)?', data_row)[0]
                if user_vlan_data[1]:
                    user_vlan_data_temp = user_vlan_data[1], user_vlan_data[0].strip(' ')
                    user_vlan_data = user_vlan_data_temp
                vlan_list.append(user_vlan_data)
                print(vlan_list)
            if data_row.startswith('access-type'):
                domain_name_list = re.findall(r'authentication (\S+)', data_row)
                if len(domain_name_list) > 0:
                    domain_name = domain_name_list[0]
            if data_row.startswith('description'):
                description = data_row.replace('description ', '')
            if data_row.startswith('vpn-instance'):
                vpn_name = data_row.replace('vpn-instance ', '')
            if data_row.startswith('dot1q termination vid'):
                dot1q_vlan = re.findall(r'dot1q termination vid (\d+)', data_row)
                dot1q_vlan += ['']
                dot1q_vlan_tuple = tuple(dot1q_vlan)
                vlan_list.append(dot1q_vlan_tuple)
            if data_row.startswith('qinq termination pe-vid'):
                qinq_vlan = re.findall(
                    r'qinq termination pe-vid (\d+) ce-vid (\d+)', data_row)
                vlan_list += qinq_vlan
            if data_row.startswith('vlan-type dot1q'):
                dot1q_vlan = re.findall(r'vlan-type dot1q (\d+)', data_row)
                dot1q_vlan += ['']
                dot1q_vlan_tuple = tuple(dot1q_vlan)
                vlan_list.append(dot1q_vlan_tuple)
            if data_row.startswith('ip address'):
                ip_address = re.findall(r'ip address (.+)', data_row)
                ip_address_list += ip_address
            if data_row.startswith('ipv6 address') and not data_row.endswith('auto link-local'):
                ipv6_address = re.findall(r'ipv6 address (.+)', data_row)
                ipv6_address_list += ipv6_address
            if data_row.startswith('qos-profile'):
                qos_profile = re.findall(
                    r'qos-profile (.+) inbound identifier none', data_row)
                if len(qos_profile) > 0:
                    qos_profile_in = qos_profile[0]
                qos_profile = re.findall(
                    r'qos-profile (.+) outbound identifier none', data_row)
                if len(qos_profile) > 0:
                    qos_profile_out = qos_profile[0]
            if data_row.startswith('shutdown'):
                shutdown = data_row
            if data_row.startswith('ip binding vpn-instance'):
                vpn_name = data_row.replace('ip binding vpn-instance ', '')
            if data_row.startswith('traffic-policy'):
                traffic_policy = data_row.replace('traffic-policy ', '')
            if data_row.startswith('mpls l2vc'):
                pw = re.findall(r'mpls l2vc ((?:\d+.){3}\d+) (\d+)', data_row)[0]
            if data_row.startswith('mtu'):
                mtu = data_row.replace('mtu ', '')
            if data_row.startswith('isis enable'):
                isis_router = data_row.replace('isis enable ', '')
            if data_row.startswith('isis ipv6 enable'):
                isis_v6_router = data_row.replace('isis ipv6 enable ', '')
            if data_row.startswith('isis circuit-type'):
                isis_type = data_row.replace('isis circuit-type ', '')
            if data_row.startswith('isis circuit-level'):
                isis_level = data_row.replace('isis circuit-level ', '')
            if data_row.startswith('isis ipv6 cost'):
                isis_v6_cost = re.findall(r'isis ipv6 cost (\d+) ?', data_row)[0]
            if data_row.startswith('isis cost'):
                isis_cost = re.findall(r'isis cost (\d+) ?', data_row)[0]
            if data_row.startswith('isis small-hello'):
                isis_small_hello = data_row.replace('isis ', '')
            if data_row.startswith('l2 binding vsi'):
                vpls_name = data_row.replace('l2 binding vsi ', '')
            if data_row.startswith('eth-trunk'):
                eth_trunk_id = re.findall(r'eth-trunk (\d+)', data_row)[0]

        intf_data_dict['intf_name'] = intf_name
        intf_data_dict['description'] = description
        intf_data_dict['vlan_list'] = vlan_list
        intf_data_dict['ip_address_list'] = ip_address_list
        intf_data_dict['ipv6_address_list'] = ipv6_address_list
        intf_data_dict['domain_name'] = domain_name
        intf_data_dict['vpn_name'] = vpn_name
        intf_data_dict['qos_profile_in'] = qos_profile_in
        intf_data_dict['qos_profile_out'] = qos_profile_out
        intf_data_dict['shutdown'] = shutdown
        intf_data_dict['vpn_name'] = vpn_name
        intf_data_dict['traffic_policy'] = traffic_policy
        intf_data_dict['pw'] = pw
        intf_data_dict['mtu'] = mtu
        intf_data_dict['isis_router'] = mtu
        intf_data_dict['isis_router'] = isis_router
        intf_data_dict['isis_v6_router'] = isis_v6_router
        intf_data_dict['isis_type'] = isis_type
        intf_data_dict['isis_level'] = isis_level
        intf_data_dict['isis_v6_cost'] = isis_v6_cost
        intf_data_dict['isis_cost'] = isis_cost
        intf_data_dict['isis_small_hello'] = isis_small_hello
        intf_data_dict['vpls_name'] = vpls_name
        intf_data_dict['eth_trunk_id'] = eth_trunk_id
        if intf_data_dict['isis_router'] != 'none' or intf_data_dict['isis_v6_router'] != 'none':
            intf_data_dict['inft_type'] = 'router_intf'
        elif len(intf_data_dict['ip_address_list']) > 0 or len(intf_data_dict['ipv6_address_list']) > 0:
            intf_data_dict['inft_type'] = 'gateway_intf'
        elif intf_data_dict['domain_name'] != 'none':
            intf_data_dict['inft_type'] = 'domain_intf'
        elif intf_data_dict['pw'] != 'none':
            intf_data_dict['inft_type'] = 'pw_intf'
        elif intf_data_dict['vpls_name'] != 'none':
            intf_data_dict['inft_type'] = 'vpls_intf'
        elif intf_data_dict['eth_trunk_id'] != 'none':
            intf_data_dict['inft_type'] = 'eth_trunk_intf'
        else:
            intf_data_dict['inft_type'] = 'other_intf'
        inft_data_dict_list.append(intf_data_dict)
    return inft_data_dict_list


def main():
    data_file = r'D:\xuexi\db\dev_data_db'
    read_data_name = 'intface_data_list'
    intface_data_list = read_data(data_file, read_data_name)

    inft_data_collect_dict = inft_data_collect(intface_data_list)
    write_data_name = 'intface_data_collect_dict_list'
    write_data(data_file, write_data_name, inft_data_collect_dict)

    csv_file_name = r'D:\xuexi\db\intf_data.csv'
    write_csv(csv_file_name, inft_data_collect_dict)


if __name__ == '__main__':
    main()
