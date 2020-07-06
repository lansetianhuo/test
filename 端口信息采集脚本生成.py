#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   端口信息采集脚本生成
@时间     :   2020-5-25 16:30
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@文件     :   csv_script.py
@时间     :   2020-4-7 16:52
@作者     :   lansetianhuo
@版本     :   1.0
@联系方式 :   24279100@qq.com
@功能     :
"""
# Start typing your code from here
import xlwings as xw
import re


def xl_read(xl_file_path, sheet_name, cell_range):
    xl_app = xw.App(visible=False, add_book=False)
    load_wb = xl_app.books.open(xl_file_path)

    load_ws = load_wb.sheets[sheet_name]

    cell_list = load_ws[cell_range].value
    load_wb.close()
    xl_app.quit()
    return cell_list


def output_file(file_path, output_str):
    with open(file_path, 'w') as file:
        file.write(output_str)





if __name__ == '__main__':
    xl_file_path = r'D:\xuexi\cheshiwenjian\富区MSE新老设备端口对应表.xlsx'
    sheet_name = 'Sheet1'
    cell_range = 'A2:A31'
    dev_name = 'HL-QQ-FQ-MSE-1.MAN.M6000#'
    data_list = xl_read(xl_file_path, sheet_name, cell_range)
    str_list = ''
    for row in data_list:
        str_list += f'''crt.Screen.Send "show opticalinfo {row}" & chr(13)
crt.Screen.WaitForString "{dev_name}" 
'''

# print(str_list)
file_path = r'D:\xuexi\cheshiwenjian\端口信息采集脚本.vbs'
output_file(file_path, str_list)
