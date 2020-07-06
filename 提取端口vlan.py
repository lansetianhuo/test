import re
s = '''interface Eth-Trunk10.43
 description to_IPTV_unicast
 trust upstream default
 user-vlan 1001 qinq 1096
 user-vlan 1001 3000
 user-vlan 1001 3000 qinq 1145 1146
 user-vlan 1001
 user-vlan 1001 3000 qinq 1216
 user-vlan 1001 3000 qinq 1242            
 user-vlan 1001 3000 qinq 1251
 user-vlan 1001 3000 qinq 1272 1273
 user-vlan 1001 3000 qinq 1277
 user-vlan 1001 3000 qinq 1344 1345
 user-vlan 1001 3000 qinq 1389
 user-vlan 1001 3000 qinq 1468
 user-vlan 1001 2000 qinq 1469
 user-vlan 1001 2000 qinq 1493
 user-vlan 1001 2000 qinq 1496
 user-vlan 1001 3000 qinq 1503
 user-vlan 1001 1500 qinq 1539
 user-vlan 1001 2000 qinq 1601
 user-vlan 1001 1200 qinq 1602
 user-vlan 1001 1600 qinq 1633
 user-vlan 1001 3000 qinq 1657
 user-vlan 1001 2800 qinq 1716 1717
 user-vlan 1001 1400 qinq 1724
 user-vlan 1001 2900 qinq 1745
 user-vlan 1001 2900 qinq 1770
 user-vlan 1001 1300 qinq 1778
 user-vlan 1001 3000 qinq 1815
 bas
 #
  access-type layer2-subscriber default-domain pre-authentication pre-iptv authentication iptv
  authentication-method ppp web
  service-identify-policy iptv
  arp-proxy
  ip-trigger
  arp-trigger
  default-user-name-template iptv
 #
'''


def vlan_collect(intf_data_list):
    vlan_re = re.compile(
        r'user-vlan\s(\d+\s?\d*)(?:\sqinq\s)?(\d*\s?\d*)')
    vlan_list = []
    for data_row in intf_data_list:
        vlan = re.findall(vlan_re, data_row)
        # 去除空列表
        if len(vlan) > 0:
            # qinq vlan 内外层标签对调，将外层VLAN放到元组的0位置上，内层VLAN放到元组的1位置上
            if vlan[0][1]:
                vlan_tuple = vlan[0][1], vlan[0][0]
                vlan = [vlan_tuple]
            # 将VLAN信息加入列表
            else:
                vlan_tuple = vlan[0][0].strip(' '), vlan[0][1]
                vlan = [vlan_tuple]
            vlan_list += vlan
    return vlan_list


def main():

    intf_data_list = s.split('\n')
    intf_vlan_list = vlan_collect(intf_data_list).copy()
    print(intf_vlan_list)


if __name__ == '__main__':
    main()
