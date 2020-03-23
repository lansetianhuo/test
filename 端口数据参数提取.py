import re
import shelve
import csv


def inft_data_collect(intf_data_set):
    inft_data_dict_list = []
    for intf_data_list in intf_data_set:
        intf_name = 'none'
        vlan_list = []
        domain_name = 'none'
        description = 'none'
        ip_address_list = []
        qos_profile_in = 'none'
        qos_profile_out = 'none'
        shutdown = 'none'
        vpn_name = 'none'
        traffic_policy = 'none'
        intf_data_dict = {}
        for data_row in intf_data_list:
            data_row = data_row.strip(' ')
            if data_row.startswith('interface'):
                intf_name = data_row.replace('interface ', '')
            if data_row.startswith('user-vlan'):
                user_vlan_data = re.split('user-vlan | qinq ', data_row)
                del user_vlan_data[0]
                if len(user_vlan_data) == 1:
                    user_vlan_data += ['']
                elif len(user_vlan_data) > 1:
                    user_vlan_data[0], user_vlan_data[1] = user_vlan_data[1], user_vlan_data[0]
                user_vlan_tuple = tuple(user_vlan_data)
                vlan_list.append(user_vlan_tuple)
            if data_row.startswith('access-type'):
                domain_name_list = re.findall(r' authentication (\w+)', data_row)
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
            if data_row.startswith('ip address'):
                ip_address = re.findall(r'ip address (.+)', data_row)
                ip_address_list += ip_address
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

        intf_data_dict['intf_name'] = intf_name
        intf_data_dict['description'] = description
        intf_data_dict['vlan_list'] = vlan_list
        intf_data_dict['ip_address_list'] = ip_address_list
        intf_data_dict['domain_name'] = domain_name
        intf_data_dict['vpn_name'] = vpn_name
        intf_data_dict['qos_profile_in'] = qos_profile_in
        intf_data_dict['qos_profile_out'] = qos_profile_out
        intf_data_dict['shutdown'] = shutdown
        intf_data_dict['vpn_name'] = vpn_name
        intf_data_dict['traffic_policy'] = traffic_policy
        inft_data_dict_list.append(intf_data_dict)
    return inft_data_dict_list


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
