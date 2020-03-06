import re
from IPy import IP, IPSet

used_ip_str_path = input('被使用IP统计文件路径：')
print(used_ip_str_path)

usable_ip_str_path = input('可用IP范围文件路径：')
print(usable_ip_str_path)

not_used_ip_str_path = input('未使用IP输出文件路径：')
print(not_used_ip_str_path)

with open(used_ip_str_path, 'r', encoding='utf-8-sig') as file_used_ip:
    used_ip_str = file_used_ip.read()

with open(usable_ip_str_path, 'r', encoding='utf-8-sig') as file_usable_ip:
    usable_ip_str = file_usable_ip.read()


# 判断字符串是否为IP函数
def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    data_list = []
    data_list = re.split('\n', data_str)
    return data_list


used_ip_list = data_format(used_ip_str)


def col_data_format(data_list):
    col_data_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        row_data = row_data.strip('\t')
        row_data = row_data.replace('\t', ' ')
        for col_data in range(row_data.find('  ')):
            row_data = row_data.replace('  ', ' ')
            col_data = range(row_data.find('  '))
        row_data = re.split(r'[ /]', row_data)
        if ip_true(row_data[0]):
            col_data_list.append(row_data)
    return col_data_list


used_ip_list = col_data_format(used_ip_list)
used_ip_net_set = []
for used_ip in used_ip_list:
    if ip_true(used_ip[0]):
        used_ip_net_set.append(IP(used_ip[0]).make_net(used_ip[1]))
# print(used_ip_net_set)

usable_ip_list = data_format(usable_ip_str)
usable_ip_set = []
for usable_ip in usable_ip_list:
    usable_ip_set.append(IP(usable_ip))
conn_ip = IPSet(usable_ip_set)
# conn_ip = IPSet([IP('112.100.107.0/24'), IP('112.100.14.0/24')])
for used_ip_net in used_ip_net_set:
    conn_ip.discard(IP(used_ip_net))
# for conn_ip_tmp in conn_ip:
#     print(conn_ip_tmp)

not_used_ip_str = ""
for not_used_ip in conn_ip:
    not_used_ip_str = not_used_ip_str + str(not_used_ip) + "\n"

with open(not_used_ip_str_path, 'w') as file_not_used_ip:
    file_not_used_ip.write(not_used_ip_str)
