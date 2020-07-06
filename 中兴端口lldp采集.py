#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   中兴端口lldp采集
@时间     :   2020-7-6 10:50
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""

def read_file(file_path):
    with open(file_path, 'r', encoding='UTF-8-sig') as file:
        data = file.readlines()
        for row in range(len(data)):
            data[row] = data[row].strip('\n')
    return data


def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)


def main():
    file_path = r'D:\xuexi\cheshiwenjian\中兴设备端口.txt'
    data_list = read_file(file_path)
    dev_name = 'HL-HEB-JY-M-1.MCN.9K8E#'
    str_list = ''
    for row in data_list:
        str_list += f'''crt.Screen.Send "show lldp entry interface {row}" & chr(13)
crt.Screen.WaitForString "{dev_name}" 
'''

    file_path = r'D:\xuexi\cheshiwenjian\中兴端口lldp采集.vbs'
    output_file(file_path, str_list)


if __name__ == '__main__':
    main()
