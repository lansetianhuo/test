#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   反掩码转换
@时间     :   2021-1-24 19:17
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    return data

def wildcard_mask_convert(wmask_set):
    wildcard_mask_set = [['127.255.255.255', '1', '128.0.0.0'],
                         ['63.255.255.255', '2', '192.0.0.0'],
                         ['31.255.255.255', '3', '224.0.0.0'],
                         ['15.255.255.255', '4', '240.0.0.0'],
                         ['7.255.255.255', '5', '248.0.0.0'],
                         ['3.255.255.255', '6', '252.0.0.0'],
                         ['1.255.255.255', '7', '254.0.0.0'],
                         ['0.255.255.255', '8', '255.0.0.0'],
                         ['0.127.255.255', '9', '255.128.0.0'],
                         ['0.63.255.255', '10', '255.192.0.0'],
                         ['0.31.255.255', '11', '255.224.0.0'],
                         ['0.15.255.255', '12', '255.240.0.0'],
                         ['0.7.255.255', '13', '255.248.0.0'],
                         ['0.3.255.255', '14', '255.252.0.0'],
                         ['0.1.255.255', '15', '255.254.0.0'],
                         ['0.0.255.255', '16', '255.255.0.0'],
                         ['0.0.127.255', '17', '255.255.128.0'],
                         ['0.0.63.255', '18', '255.255.192.0'],
                         ['0.0.31.255', '19', '255.255.224.0'],
                         ['0.0.15.255', '20', '255.255.240.0'],
                         ['0.0.7.255', '21', '255.255.248.0'],
                         ['0.0.3.255', '22', '255.255.252.0'],
                         ['0.0.1.255', '23', '255.255.254.0'],
                         ['0.0.0.255', '24', '255.255.255.0'],
                         ['0.0.0.127', '25', '255.255.255.128'],
                         ['0.0.0.63', '26', '255.255.255.192'],
                         ['0.0.0.31', '27', '255.255.255.224'],
                         ['0.0.0.15', '28', '255.255.255.240'],
                         ['0.0.0.7', '29', '255.255.255.248'],
                         ['0.0.0.3', '30', '255.255.255.252'],
                         ['0.0.0.1', '31', '255.255.255.254'],
                         ['0.0.0.0', '32', '255.255.255.255'],
                         ['0', '32', '255.255.255.255']]
    wmask_list = []
    for wmask_data in wmask_set:
        for wmask in wildcard_mask_set:
            if wmask_data[1] == wmask[0]:
               wmask_data[1] = wmask[1]
        wmask_list.append(wmask_data)
    return wmask_list





def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False

def data_format(data_str):
    data_str = data_str.strip(' ')
    data_str = data_str.strip('\n')
    data_list = re.split('\n', data_str)
    return data_list



def col_data_format(data_list):
    col_data_list = []
    for row_data in data_list:
        row_data = row_data.strip(' ')
        row_data = row_data.strip('\t')
        row_data = row_data.replace('\t', ' ')
        for col_data in range(row_data.find('  ')):
            row_data = row_data.replace('  ', ' ')
            # col_data = range(row_data.find('  '))
        row_data = re.split(r'[ /]',row_data)
        if ip_true(row_data[0]):
            col_data_list.append(row_data)
    return col_data_list

def ip_format(ip_list):
    ip_set = []
    for ip_element in ip_list:
        if ip_true(ip_element[0]):
            ip_set.append(ip_element[0])
    return ip_set

def ip_list_str(data_list):
    output_str = ""
    for data_element in data_list:
        output_str = output_str + str(data_element[0])+"/"+ str(data_element[
                                                                    1]) + "\n"
    return output_str

def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)
def main():
    file_path = r'D:\xuexi\cheshiwenjian\学府FW01-地址集-i.txt'
    out_file_path = r'D:\xuexi\cheshiwenjian\学府FW01-IP地址集表.txt'
    ip_wmask_str= read_file(file_path)
    ip_wmask_list= data_format(ip_wmask_str).copy()
    ip_wmask_list = col_data_format(ip_wmask_list).copy()
    wildcard_mask_set = wildcard_mask_convert(ip_wmask_list)


    ip_str = ip_list_str(wildcard_mask_set)
    output_file(out_file_path, ip_str)



if __name__ == '__main__':
    main()