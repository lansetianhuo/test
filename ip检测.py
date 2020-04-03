#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   ip检测
@时间     :   2020-4-3 17:35
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re


def ip_true(port_ip):
    ip_rule = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)/\d{1,2}$')
    if ip_rule.match(port_ip):
        return True
    else:
        return False


def main():
    print(ip_true('0.0.0.000/'))


if __name__ == '__main__':
    main()
