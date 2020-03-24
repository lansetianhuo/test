#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   配置文件分片-存在shelve中
@时间     :   2020-3-24 11:46
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here

# 用于引用分融函数
import re
import shelve


# 创建配置文切片函数
def configfile_section_function(configfile, configfile_delimiter, useless_data):
    """
    创建配置文切片函数，将配置文件按回车分隔成元素存入列表configfile_list，对元素进行格式化，
    再按配置文件切片分隔符对列表查行切片，并存储在列表configfile_section_format_set中。
    函数有三个参数：
    configfile：配置文件内容，用于将配置文件内容以字符串形式传递给函数处理；
    configfile_delimiter：配置文件切片分隔符，定义以什么字符作为配置文件切片分隔符；
    useless_data：定义以什么字符作为行开头要清理掉的无用数据
    """

    # 去除配置文件字符串中前、后空格
    configfile = configfile.strip()
    # 配置文件按回车分隔成元素存入列表configfile_list
    configfile_list = re.split('\n', configfile)
    # 创建配置数据分片列表，并赋值为空。
    configfile_section_list = []
    # 创建分片元素开始索引，并赋值为0，从第一个开始。
    section_start_index = 0
    # 对配置列表按配置文件切片分隔符进行切片(以元素开头为分隔符的进行切片)
    for element_index in range(len(configfile_list)):
        if configfile_list[element_index].startswith(configfile_delimiter):
            # 将切片存入列表peizhi_qiepian
            configfile_section_list.append(
                configfile_list[section_start_index:element_index])
            # 将元素开始索引变为当前索值
            section_start_index = element_index
    # 创建配置切片格式化数据临时列表变量
    configfile_section_format = []
    # 创建配置切片格式化后数据速查存储列表变量
    configfile_section_format_set = []
    # 对配置切片中数据进行整理
    for configfile_section_sub in configfile_section_list:
        for configfile_section_element in configfile_section_sub:
            # 去除元素前、后空格
            configfile_section_element = configfile_section_element.strip()
            # 通过列表转存的方式去除以useless_data变量内容开头的无用数据
            if not configfile_section_element.startswith(useless_data):
                # 去除内容为空的元素
                if len(configfile_section_element):
                    # 将configfile_zone_element内容转存到configfile_zone_format
                    configfile_section_format.append(configfile_section_element)
        # 去除内容为空的元素
        if len(configfile_section_format):
            # 将configfile_zone_format内容转存到configfile_zone_format_set
            configfile_section_format_set.append(configfile_section_format)
        # 将configfile_zone_format处空，用于下一个循使用
        configfile_section_format = []
    # 返回完成切片的配置数据列表，函数返回值
    return configfile_section_format_set


def write_data(file_name, data_name, data):
    stud_db = shelve.open(file_name)
    stud_db[data_name] = data
    stud_db.close()


def main():
    # 定义文件输入路径变量,r为避免使用反义字符
    file_path = r'D:\xuexi\cheshiwenjian\1.txt'

    # 将文件以字符串形式赋值给变量configfile，以'UTF-8-sig'格式打开文件
    with open(file_path, 'rt', encoding='UTF-8-sig') as file:
        configfile = file.read()

    # 定义以什么字符作为配置文件切片分隔符
    configfile_delimiter = "#"
    # 定义以什么字符作为行开头要清理掉的无用数据
    useless_data = "#"

    # 调用配置文件切片函数对配置文件数据进行处理
    configfile_section_result = configfile_section_function(configfile, configfile_delimiter,
                                                            useless_data)

    write_data(r'D:\xuexi\db\dev_data_db', 'dev_data_list', configfile_section_result)


if __name__ == '__main__':
    main()
