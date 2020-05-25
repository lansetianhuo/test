#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   端口信息采集脚本生成-文本
@时间     :   2020-5-25 17:01
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""


# Start typing your code from here
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
    file_path = r'D:\xuexi\cheshiwenjian\新端口.txt'
    data_list = read_file(file_path)
    dev_name = 'HL-QQ-FQ-MSE-1.MAN.M6000#'
    str_list = ''
    for row in data_list:
        str_list += f'''crt.Screen.Send "show opticalinfo {row}" & chr(13)
crt.Screen.WaitForString "{dev_name}" 
'''

    file_path = r'D:\xuexi\cheshiwenjian\端口信息采集脚本1.vbs'
    output_file(file_path, str_list)


if __name__ == '__main__':
    main()
