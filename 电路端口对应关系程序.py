import re
# 导入IP处理模块
from IPy import IP

local_ip_path = r"D:\xuexi\cheshiwenjian\本端ip.txt"
remote_ip_path = r"D:\xuexi\cheshiwenjian\14.17.txt"

with open(local_ip_path, 'r', encoding='utf-8-sig') as file_local_ip:
    local_data = file_local_ip.readlines()
with open(remote_ip_path, 'r', encoding='utf-8-sig') as file_remote_ip:
    remote_data = file_remote_ip.readlines()
# print(remote_data)


# 判断字符串是否为IP函数
def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


# 文件输入端口对应IP数据格式化函数
def intface_format(intf_data):
    intf_list = []
    for intf in intf_data:
        intf = intf.split()
        intf = intf[:2] + intf[2].split('/')
        if ip_true(intf[2]):
            intf_list.append(intf)
    return intf_list


local_intf_list = intface_format(local_data.copy())

remote_intf_list = intface_format(remote_data.copy())

# 两台设备端口IP匹配函数
intf_to_intf_data = []
for local_ip in local_intf_list:
    intf_to_intf = ""
    for remote_ip in remote_intf_list:
        if IP(remote_ip[2]) in IP(local_ip[2]).make_net(local_ip[3]):
            intf_to_intf = '_'.join(local_ip[:3]) + "_" + "_".join(
                remote_ip[:3])
            intf_to_intf_data.append(intf_to_intf)

# 将匹配出来的设备端口对应关系存入字符串中，以便输出来文件
intf_to_intf_data_str = ""
for row_data in intf_to_intf_data:
    intf_to_intf_data_str = intf_to_intf_data_str + str(row_data) + "\n"

intf_to_intf_path = r"D:\xuexi\cheshiwenjian\端口对应关系表.txt"
with open(intf_to_intf_path, 'w') as file_intf_to_intf:
    file_intf_to_intf.write(intf_to_intf_data_str)
