import re
# 导入IP处理模块
from IPy import IP

#
local_ip_path = input('本端端口文件路径：')
# local_ip_path = r"D:\xuexi\cheshiwenjian\本端及IP信息.txt"
print(local_ip_path)

remote_ip_path = input('对端端口文件路径：')
# remote_ip_path = r"D:\xuexi\cheshiwenjian\对端及IP信息.txt"
print(remote_ip_path)

intf_to_intf_path = input('输出端口对应文件路径：')
# intf_to_intf_path = r"D:\xuexi\cheshiwenjian\端口对应关系表.txt"
print(intf_to_intf_path)

# 输入本端设备名
local_device_name = input('本端设备名：')
print(local_device_name)

# 输入对端设备名
remote_device_name = input('对端设备名：')
print(remote_device_name)

with open(local_ip_path, 'r', encoding='utf-8-sig') as file_local_ip:
    local_data = file_local_ip.read()
with open(remote_ip_path, 'r', encoding='utf-8-sig') as file_remote_ip:
    remote_data = file_remote_ip.read()


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
    intf_data = intf_data.strip(' ')
    intf_data = intf_data.strip('\n')
    intf_list = []
    intf_data_list = re.split('\n', intf_data)
    for intf in intf_data_list:
        intf = intf.strip(' ')
        intf = intf.strip('\t')
        intf = intf.replace('\t', ' ')
        for col_data in range(intf.find('  ')):
            intf = intf.replace('  ', ' ')
            col_data = range(intf.find('  '))
        intf = re.split(r'[ ]', intf)
        intf = intf[:1] + re.split('/', str(intf[1]))
        if ip_true(intf[1]):
            intf_list.append(intf)
    return intf_list


local_intf_list = intface_format(local_data)
remote_intf_list = intface_format(remote_data)

# 两台设备端口IP匹配函数
intf_to_intf_data = []
for local_ip in local_intf_list:
    intf_to_intf = ""
    for remote_ip in remote_intf_list:
        if IP(remote_ip[1]) in IP(local_ip[1]).make_net(local_ip[2]):
            intf_to_intf = local_device_name + "_" + '_'.join(
                local_ip[:2]) + "_" + remote_device_name + "_" + "_".join(
                    remote_ip[:2])
            intf_to_intf_data.append(intf_to_intf)

# 将匹配出来的设备端口对应关系存入字符串中，以便输出来文件
intf_to_intf_data_str = ""
for row_data in intf_to_intf_data:
    intf_to_intf_data_str = intf_to_intf_data_str + str(row_data) + "\n"

with open(intf_to_intf_path, 'w') as file_intf_to_intf:
    file_intf_to_intf.write(intf_to_intf_data_str)
