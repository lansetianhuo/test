import re

lldp_path = r"D:\xuexi\cheshiwenjian\lldp_m6000.txt"

with open(lldp_path, 'r', encoding='utf-8-sig') as file_lldp:
    lldp_data = file_lldp.read()

lldp_data = lldp_data.strip(' ')

lldp_data_list = re.split(
    '--------------------------------------------------------', lldp_data)

lldp_sub_set = []
for lldp_data_Section in lldp_data_list:
    lldp_data_Section_list = re.split('\n', lldp_data_Section)
    lldp_sub = []
    for lldp_data_row in lldp_data_Section_list:
        lldp_data_row = lldp_data_row.strip(' ')
        if lldp_data_row != '':
            lldp_sub.append(lldp_data_row)
    lldp_sub_set.append(lldp_sub)

inft_data_set = ""
for intf_data in lldp_sub_set:
    if intf_data[0].startswith('Local Port:'):
        remote_dev = "none"
        remote_port = "none"
        for intf_data_sub in intf_data:
            if intf_data_sub.startswith('Local Port:'):
                intf_port = re.split(r' ', intf_data_sub)[2]
            elif intf_data_sub.startswith('System Name:'):
                remote_dev = intf_data_sub.replace('System Name:',
                                                   '').strip(' ')
            elif intf_data_sub.startswith('Peer Port:'):
                remote_port = intf_data_sub.replace('Peer Port:', '')
                remote_port = remote_port.replace('| Interface Name',
                                                  '').strip(' ')
        inft_data_set = inft_data_set + str(
            intf_port) + " " + remote_dev + " " + remote_port + "\n"

lldp_fin_path = r"D:\xuexi\cheshiwenjian\lldp_fin.txt"

with open(lldp_fin_path, 'w') as file_fin_lldp:
    file_fin_lldp.write(inft_data_set)
