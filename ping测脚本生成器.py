#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   ping测脚本生成器
@时间     :   2021-1-28 16:33
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
    file_path = r'D:\xuexi\cheshiwenjian\ping测ip.txt'
    data_list = read_file(file_path)
    dev_name = '<HL-QQ-WH-MSE-1.MAN.ME60>'
    vpn_name = 'CTVPN2521103'
    str_list = ''
    if vpn_name =="":
        for row in data_list:
            str_list += f'''crt.Screen.Send "ping -m 2 -c 1 {row}" & chr(13)
crt.Screen.WaitForString "{dev_name}"
'''
    else:
        for row in data_list:
            str_list += f'''crt.Screen.Send "ping -m 2 -c 1 -vpn-instance {vpn_name} {row}" & chr(13)
crt.Screen.WaitForString "{dev_name}"
'''

    file_path = r'D:\xuexi\cheshiwenjian\ping测脚本.vbs'
    output_file(file_path, str_list)


if __name__ == '__main__':
    main()
