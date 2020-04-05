#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   ipv6判断
@时间     :   2020-4-5 15:10
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import re


def ipv6_addr(addr):

    ip6_regex = '(?:(?:[0-9a-fA-F]{0,4}):){1,7}(?::?[0-9a-fA-F]{1,4})?'
    return bool(re.match(ip6_regex, addr))


if __name__ == '__main__':
    print(ipv6_addr('240E:0:0:FFFF::184'))
