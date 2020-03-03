#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File    :   zte_shebei_duankou_tihuan.py
@Time    :   2020/03/03 16:46:36
@Author  :   lanse
@Version :   1.0
@Contact :   @qq.com
@WebSite :
'''
# Start typing your code from here
import re
"""
本程序用来对网络设备配置的端口进行替换操作，主要用来对同型号的网络设备替换时成生成新设备的配置文件。
目前支持华为、中兴的MSE、CR，ER设备同型号设备替换
可替换端口名内容：
中兴设备：所有以“interface+端口名”格式配置中的端口名; 静态路由配置绑定的端口名；静态用户绑定的端口名；
ISIS、MPLS、OSPF、PIM、port-acl、supervlan配置中的端口名；用户端口限速绑定的端口名；l2vpn绑定的端口名。

使用说明：
将老、新设备的端口对应关系以每个对应关系为一行的形式存入"端口关系.txt"文件，并把文件路径赋值给duankou_path变量
duankou_path = "D:\\xuexi\\cheshiwenjian\\端口关系.txt"
文件格式如下：
xgei-0/1/0/0 xgei-0/2/0/0
xgei-0/1/0/1 xgei-0/2/0/1
xgei-0/1/1/4 xgei-0/2/1/4
xgei-0/2/0/0 xgei-0/3/0/0
xgei-0/2/0/1 xgei-0/4/0/1
前面是老设备端口，后面是新设备端口，中间用空格分开。

将老设备配置从设备上采集下来存入"设备配置.txt"文件，并把文件路径赋值给peizhi_lujing变量
peizhi_lujing = "D:\\xuexi\\cheshiwenjian\\设备配置.txt"

执行该程序

最终端口名称替换后的配置文件内容写入文件
tihuan_peizhi_lujin = "D:\\xuexi\\cheshiwenjian\\端口替换后配置.txt"
文件文件路径变量中的内容可按实际需要修改。
"""


def duankou_guanxi_yuanzu(duankou):
    """
    本函数为新、老端口对关系列表处理函数，用于把端口对应该处理成元组，以便替换端口函数调用该元组。
    使用元组存储端口对应关系以确保在程序通行时，端口对应关系不会被修改。
    函数有一个参数：
    duankou：将新、老端口对关系文件以字符串形式传给该函数，
    函数返回一个值：
    duankou_yuanzu：为新、老端口对关系元组。
    """
    duankou_liebiao = []
    duankou_biao = re.split('\n', duankou)
    for duankou_guanxi in duankou_biao:
        duankou_guanxi = duankou_guanxi.strip(' ')
        duankou_guanxi = duankou_guanxi.strip('\t')
        duankou_guanxi = duankou_guanxi.replace('\t', ' ')
        for guanxi_xuhao in range(duankou_guanxi.find('  ')):
            duankou_guanxi = duankou_guanxi.replace('  ', ' ')
            guanxi_xuhao = range(duankou_guanxi.find('  '))
        duankou_guanxi = re.split(' ', duankou_guanxi)
        duankou_liebiao.append(tuple(duankou_guanxi))
    duankou_yuanzu = tuple(duankou_liebiao)
    return duankou_yuanzu


def tihuan_duankou(peizhi, duankou_guanxibiao):
    """
    本函数为替换文件中端口名称的函数。
    函数有两个参数：
    peizhi：将要修改端口的配置文件以字符串形式传给该函数
    duankou_guanxibiao：将新、老端口对关系元组传给该函数
    函数返回一个值：
    duankou_tihuan_peizhi：返回端口名称替换后的配置文件列表
    """
    peizhi_liebiao = re.split('\n', peizhi)
    duankou_tihuan_peizhi = []
    for peizhi_yuansu in peizhi_liebiao:
        peizhi_yuansu_tmp = peizhi_yuansu.strip(' ')
        if str(peizhi_yuansu_tmp).startswith('interface'):
            # 判断元素是否为'interface'(如端口名定义）开始并修改interface后的端口名
            peizhi_yuansu_tmp = re.split(r'[ .]', peizhi_yuansu_tmp)
            for guanxi in duankou_guanxibiao:
                if str(peizhi_yuansu_tmp[1]) == guanxi[0]:
                    peizhi_yuansu = peizhi_yuansu.replace(
                        peizhi_yuansu_tmp[1], guanxi[1])
        if str(peizhi_yuansu_tmp).startswith('ip route'):
            # 判断元素是否为静态路由配置并修改指定了端口的静态路由中相应端口名
            peizhi_yuansu_tmp = re.split(r'[ .]', peizhi_yuansu_tmp)
            if peizhi_yuansu_tmp[2] == 'vrf':
                if len(peizhi_yuansu_tmp) >= 13:
                    for guanxi in duankou_guanxibiao:
                        if str(peizhi_yuansu_tmp[12]) == guanxi[0]:
                            peizhi_yuansu = peizhi_yuansu.replace(
                                peizhi_yuansu_tmp[12], guanxi[1])
            else:
                if len(peizhi_yuansu_tmp) >= 11:
                    for guanxi in duankou_guanxibiao:
                        if str(peizhi_yuansu_tmp[10]) == guanxi[0]:
                            peizhi_yuansu = peizhi_yuansu.replace(
                                peizhi_yuansu_tmp[10], guanxi[1])
        if str(peizhi_yuansu_tmp).startswith('ipv6 route'):
            # 判断元素是否为ipv6静态路由配置并修改指定了端口的静态路由中相应端口名
            peizhi_yuansu_tmp = re.split(r'[ .]', peizhi_yuansu_tmp)
            if peizhi_yuansu_tmp[2] == 'vrf':
                if len(peizhi_yuansu_tmp) >= 6:
                    for guanxi in duankou_guanxibiao:
                        if str(peizhi_yuansu_tmp[5]) == guanxi[0]:
                            peizhi_yuansu = peizhi_yuansu.replace(
                                peizhi_yuansu_tmp[5], guanxi[1])
            else:
                if len(peizhi_yuansu_tmp) >= 4:
                    for guanxi in duankou_guanxibiao:
                        if str(peizhi_yuansu_tmp[3]) == guanxi[0]:
                            peizhi_yuansu = peizhi_yuansu.replace(
                                peizhi_yuansu_tmp[3], guanxi[1])
        if str(peizhi_yuansu_tmp).startswith('service-policy'):
            # 判断元素是否为端口限速配置并修改端口限速配置中相应端口名
            peizhi_yuansu_tmp = re.split(r'[ .]', peizhi_yuansu_tmp)
            for guanxi in duankou_guanxibiao:
                if str(peizhi_yuansu_tmp[1]) == guanxi[0]:
                    peizhi_yuansu = peizhi_yuansu.replace(
                        peizhi_yuansu_tmp[1], guanxi[1])
        if str(peizhi_yuansu_tmp).startswith('ip-host'):
            # 判断元素是否为静态用户配置并修改指定了端口的静态用户配置中相应端口名
            peizhi_yuansu_tmp = re.split(r'[ ]', peizhi_yuansu_tmp)
            # 判断元素是否为ip地址
            ip_host_ip = re.compile(
                '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
            )
            tmp_num = 0
            for tmp_num in range(len(peizhi_yuansu_tmp)):
                if ip_host_ip.match(peizhi_yuansu_tmp[tmp_num]):
                    peizhi_yuansu_tmp_num = tmp_num
            peizhi_yuansu_tmp_num += 1
            peizhi_yuansu_tmp = re.split(
                r'[.]', peizhi_yuansu_tmp[peizhi_yuansu_tmp_num])
            for guanxi in duankou_guanxibiao:
                if str(peizhi_yuansu_tmp[0]) == guanxi[0]:
                    peizhi_yuansu = peizhi_yuansu.replace(
                        peizhi_yuansu_tmp[0], guanxi[1])
        if str(peizhi_yuansu_tmp).startswith('access-point'):
            # 判断元素是否为l2vpn的接入端口配置，并修改l2vpn的接入端口配置中相应端口名
            peizhi_yuansu_tmp = re.split(r'[ .]', peizhi_yuansu_tmp)
            for guanxi in duankou_guanxibiao:
                if str(peizhi_yuansu_tmp[1]) == guanxi[0]:
                    peizhi_yuansu = peizhi_yuansu.replace(
                        peizhi_yuansu_tmp[1], guanxi[1])
        duankou_tihuan_peizhi.append(peizhi_yuansu)
    return duankou_tihuan_peizhi


duankou_path = r"D:\xuexi\cheshiwenjian\端口关系.txt"
with open(duankou_path, 'r', encoding='utf-8-sig') as file_duankou:
    duankou = file_duankou.read()

duankou_guanxibiao = duankou_guanxi_yuanzu(duankou)

peizhi_lujing = r"D:\xuexi\cheshiwenjian\设备配置.txt"
with open(peizhi_lujing, 'r', encoding='utf-8-sig') as peizhi_wanjian:
    peizhi = peizhi_wanjian.read()

duankou_tihuan_jieguo = tihuan_duankou(peizhi, duankou_guanxibiao)

# 端口名称替换后的配置文件列表以字符串形式存入变量tihuan_peizhi
tihuan_peizhi = ""
for tihuan_peizhi_tmp in duankou_tihuan_jieguo:
    tihuan_peizhi = tihuan_peizhi + str(tihuan_peizhi_tmp) + "\n"

# 端口名称替换后的配置文件内容写入文件
tihuan_peizhi_lujin = r"D:\xuexi\cheshiwenjian\端口替换后配置.txt"
with open(tihuan_peizhi_lujin, 'w') as tihuan_peizhi_wenjian:
    tihuan_peizhi_wenjian.write(tihuan_peizhi)
print()
