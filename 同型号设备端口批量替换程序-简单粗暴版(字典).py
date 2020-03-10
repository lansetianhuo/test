#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@文件     :   同型号设备端口批量替换程序-简单粗暴版(字典).py
@时间     :   2020/03/10 09:40:31
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
'''
# Start typing your code from here


import re
"""
本程序用来对网络设备配置的端口进行替换操作，主要用来对同型号的网络设备替换时成生成新设备的配置文件。
目前支持华为、中兴的MSE、CR，ER设备同型号设备替换
可替换配置文件中的端口名内容：

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
# 端口关系文件路径变量
duankou_path = r"D:\xuexi\cheshiwenjian\端口关系.txt"
# 将端口关系文件信息存入变量duankou
with open(duankou_path, 'r', encoding='utf-8-sig') as file_duankou:
    duankou = file_duankou.read()

# 配置文件路径变量
peizhi_lujing = r"D:\xuexi\cheshiwenjian\设备配置.txt"
# 将配置文件文件信息存入变量peizhi
with open(peizhi_lujing, 'r', encoding='utf-8-sig') as peizhi_wanjian:
    peizhi = peizhi_wanjian.read()


def duankou_guanxi_yuanzu(duankou):
    """
    本函数为新、老端口对关系列表处理函数，用于把端口对应该处理成字典，以便替换端口函数调用该端口对应关系字典，
    键为老设备端口、值为新设备端口。
    使用字典存储端口对应关系以简化端口对应关系查找部分程序。
    函数有一个参数：
    duankou：将新、老端口对关系文件以字符串形式传给该函数，
    函数返回一个值：
    duankou_dict：为新、老端口对关系字典。
    """
    duankou_dict = {}
    duankou_biao = re.split('\n', duankou)
    for duankou_guanxi in duankou_biao:
        duankou_guanxi = duankou_guanxi.strip(' ')
        duankou_guanxi = duankou_guanxi.strip('\t')
        duankou_guanxi = duankou_guanxi.replace('\t', ' ')
        for guanxi_xuhao in range(duankou_guanxi.find('  ')):
            duankou_guanxi = duankou_guanxi.replace('  ', ' ')
            guanxi_xuhao = range(duankou_guanxi.find('  '))
        duankou_guanxi = re.split(' ', duankou_guanxi)
        duankou_dict_yuansu = {duankou_guanxi[0]: duankou_guanxi[1]}
        duankou_dict.update(duankou_dict_yuansu)
    return duankou_dict


def tihuan_duankou(peizhi, duankou_guanxibiao):
    """
    本函数为替换文件中端口名称的函数。
    函数有两个参数：
    peizhi：将要修改端口的配置文件以字符串形式传给该函数
    duankou_guanxibiao：将新、老端口对关系字典传给该函数
    函数返回一个值：
    duankou_tihuan_peizhi：返回端口名称替换后的配置文件列表
    """
    # 以换行符为分隔符将字符串分隔成列表
    peizhi_liebiao = (re.split('\n', peizhi))
    # 将列表转换成元组，以免程序处理时误修改原配置中数据
    peizhi_liebiao = tuple(peizhi_liebiao)
    # 定义元组变量，用于存储替换后的配置信息
    duankou_tihuan_peizhi = ()
    # 从原配置元组逐一取出元素
    for peizhi_yuansu in peizhi_liebiao:
        # 将原配置元素以以空格和.号为分隔符将字符串分隔成列表
        peizhi_yuansu = re.split(r'([ .])', peizhi_yuansu)
        # 将列表转换成元组，以免程序处理时误修改原配置中数据
        peizhi_yuansu = tuple(peizhi_yuansu)
        # 定义元素临时存储变量，用于存储处理后的配置信息
        hangshuju = ""
        for peizhi_yuansu_neirong in peizhi_yuansu:
            # 用元素作为字典键在端口关系字典中查找，如果有则用相应键替换peizhi_yuansu_neirong中的值，
            # 如果没有返回none，if语句不成立，对peizhi_yuansu_neirong中值不作处理。
            if duankou_guanxibiao.get(peizhi_yuansu_neirong, 'none') != 'none':
                peizhi_yuansu_neirong = duankou_guanxibiao[
                    peizhi_yuansu_neirong]
            # 将peizhi_yuansu_neirong中的值拼接成字符串hangshuju
            hangshuju = hangshuju + peizhi_yuansu_neirong
        # 将hangshuju字符串变换成元组，拼接成要返回的元组duankou_tihuan_peizhi
        duankou_tihuan_peizhi = duankou_tihuan_peizhi + tuple([hangshuju])
    return duankou_tihuan_peizhi


duankou_guanxibiao = duankou_guanxi_yuanzu(duankou)
duankou_tihuan_jieguo = tihuan_duankou(peizhi, duankou_guanxibiao)

# 端口名称替换后的配置文件元组以字符串形式存入字符串变量tihuan_peizhi
tihuan_peizhi = ""
for tihuan_peizhi_tmp in duankou_tihuan_jieguo:
    tihuan_peizhi = tihuan_peizhi + str(tihuan_peizhi_tmp) + "\n"

# 端口名称替换后的配置文件内容写入文件
tihuan_peizhi_lujin = r"D:\xuexi\cheshiwenjian\端口替换后配置.txt"
with open(tihuan_peizhi_lujin, 'w') as tihuan_peizhi_wenjian:
    tihuan_peizhi_wenjian.write(tihuan_peizhi)
