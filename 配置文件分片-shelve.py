#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   配置文件分片-shelve.py
@时间     :   2020-3-23 18:30
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here

# 用于引用分融函数
import re
import shelve

# 定义文件输入路径变量,r为避免使用反义字符
wenjian_path = r'D:\xuexi\cheshiwenjian\1.txt'

# 将文件以字符串形式赋值给变量peizhi，以'UTF-8-sig'格式打开文件
with open(wenjian_path, 'rt', encoding='UTF-8-sig') as wenjian:
    peizhi = wenjian.read()

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

    # 去除配置文件字符串中前、后空格
    peizhi = peizhi.strip()
    # 配置文件按回车分隔成元素存入列表peizhi_liebiao
    peizhi_liebiao = re.split('\n', peizhi)
    # 创建配置数据分片列表，并赋值为空。
    peizhi_qiepian = []
    # 创建分片元素开始索引，并赋值为0，从第一个开始。
    yuansu_start_suoyin = 0
    # 对配置列表按配置文件切片分隔符进行切片(以元素开头为分隔符的进行切片)
    for yuansu_suoyin in range(len(peizhi_liebiao)):
        if peizhi_liebiao[yuansu_suoyin].startswith(peizhi_qiepian_biaoshifu):
            # 将切片存入列表peizhi_qiepian
            peizhi_qiepian.append(
                peizhi_liebiao[yuansu_start_suoyin:yuansu_suoyin])
            # 将元素开始索引变为当前索值
            yuansu_start_suoyin = yuansu_suoyin
    # 创建配置切片格式化数据临时列表变量
    peizhi_qiepian_geishihua = []
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
                    # 将peizhi_qiepian_yuansu内容转存到peizhi_qiepian_geishihua
                    peizhi_qiepian_geishihua.append(peizhi_qiepian_yuansu)
        # 去除内容为空的元素
        if len(peizhi_qiepian_geishihua):
            # 将peizhi_qiepian_geishihua内容转存到peizhi_qiepian_geishihua_jihe
            peizhi_qiepian_geishihua_jihe.append(peizhi_qiepian_geishihua)
        # 将peizhi_qiepian_geishihua处空，用于下一个循使用
        peizhi_qiepian_geishihua = []
    # 返回完成切片的配置数据列表，函数返回值
    return peizhi_qiepian_geishihua_jihe


def write_data(file_name, data_name, data):
    stud_db = shelve.open(file_name)
    stud_db[data_name] = data
    stud_db.close()


# 调用配置文件切片函数对配置文件数据进行处理
peizhi_qiepian_jieguo = qiepian_hansu(peizhi, peizhi_qiepian_biaoshifu,
                                      wuyingshuju)
# print(peizhi_qiepian_jieguo)
write_data(r'D:\xuexi\db\dev_data_db', 'dev_data_list', peizhi_qiepian_jieguo)
# 定义文件输出路径变量
# shuchuwenjian_path = r'D:\xuexi\cheshiwenjian\dev_data.txt'

# 将切片的配置文件数据以字符串形式存入文件
# with open(shuchuwenjian_path, 'w') as shujuwenjian:
#     for shuju_neirong in peizhi_qiepian_jieguo:
#         shujuwenjian.write(str(shuju_neirong) + "\n")
