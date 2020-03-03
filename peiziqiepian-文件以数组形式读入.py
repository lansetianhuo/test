#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File    :   peizhiqiepian.py
@Time    :   2020/02/29 16:27:16
@Author  :   lanse
@Version :   1.0
@Contact :   @qq.com
@WebSite :
'''
# Start typing your code from here

# 定义文件输入路径变量,r为避免使用反义字符
wenjian_path = r'D:\xuexi\cheshiwenjian\1.txt'

# 将文件以字符串形式赋值给变量peizhi，以'UTF-8-sig'格式打开文件
with open(wenjian_path, 'r', encoding='UTF-8-sig') as wenjian:
    peizhi = wenjian.readlines()

# 定义以什么字符作为配置文件切片分隔符
peizhi_qiepian_biaoshifu = "#"
# 定义以什么字符作为行开头要清理掉的无用数据
wuyingshuju = "#"


# 创建配置文切片函数
def qiepian_hansu(peizhi, peizhi_qiepian_piaoshifu, wuyingshuju):
    """
    创建配置文切片函数，将配置文件按回车分隔成元素存入列表peizhi_liebiao，对元素进行格式化，
    再按配置文件切片分隔符对列表查行切片，并存储在列表peizhi_qiepian_geishihua_jihe中。
    函数有三个参数：
    peizhi：配置文件内容，用于将配置文件内容以字符串形式传递给函数处理；
    peizhi_qiepian_piaoshifu：配置文件切片分隔符，定义以什么字符作为配置文件切片分隔符；
    wuyingshuju：定义以什么字符作为行开头要清理掉的无用数据
    """
    # 创建配置数据分片列表，并赋值为空。
    peizhi_qiepian = []
    # 创建分片元素开始索引，并赋值为0，从第一个开始。
    yuansu_start_suoyin = 0
    # 对配置列表按配置文件切片分隔符进行切片(以元素开头为分隔符的进行切片)
    for yuansu_suoyin in range(len(peizhi)):
        peizhi[yuansu_suoyin].strip('\n')
        if peizhi[yuansu_suoyin].startswith(peizhi_qiepian_biaoshifu):
            # 将切片存入列表peizhi_qiepian
            peizhi_qiepian.append(peizhi[yuansu_start_suoyin:yuansu_suoyin])
            # 将元素开始索引变为当前索值
            yuansu_start_suoyin = yuansu_suoyin
    # 创建配置切片格式化数据临时字符串变量
    peizhi_qiepian_geishihua = ""
    # 创建配置切片格式化后数据速查存储列表变量
    peizhi_qiepian_geishihua_jihe = []
    # 对配置切片中数据进行整理
    for peizhi_qiepian_ziji in peizhi_qiepian:
        for peizhi_qiepian_yuansu in peizhi_qiepian_ziji:
            # 去除元素前、后空格
            peizhi_qiepian_yuansu = peizhi_qiepian_yuansu.strip()
            # 通过列表转存的方式去除以wuyingshuju变量内容开头的无用数据
            if not peizhi_qiepian_yuansu.startswith(wuyingshuju):
                # 去除内容为空的元素
                if len(peizhi_qiepian_yuansu):
                    # 将元素以字符形式存入peizhi_qiepian_geishihua变量，并设置以","号为分隔符
                    peizhi_qiepian_geishihua = peizhi_qiepian_geishihua + str(
                        peizhi_qiepian_yuansu) + ","
        # 去除整段字符串前、后的","号
        peizhi_qiepian_geishihua = peizhi_qiepian_geishihua.strip(',')
        # 去除内容为空的元素
        if len(peizhi_qiepian_geishihua):
            # 将peizhi_qiepian_geishihua内容转存到peizhi_qiepian_geishihua_jihe
            peizhi_qiepian_geishihua_jihe.append(peizhi_qiepian_geishihua)
        # 将peizhi_qiepian_geishihua处空，用于下一个循使用
        peizhi_qiepian_geishihua = ""
    # 返回完成切片的配置数据列表，函数返回值
    return peizhi_qiepian_geishihua_jihe


# 调用配置文件切片函数对配置文件数据进行处理
peizhi_qiepian_jieguo = qiepian_hansu(peizhi, peizhi_qiepian_biaoshifu,
                                      wuyingshuju)
# 定义文件输出路径变量
shuchuwenjian_path = r'D:\xuexi\cheshiwenjian\4.txt'
# 将切片的配置文件数据以字符串形式存入文件
with open(shuchuwenjian_path, 'w') as shujuwenjian:
    for shuju_neirong in peizhi_qiepian_jieguo:
        shujuwenjian.write(shuju_neirong + "\n")
