import re
duankou_peizhi = """
端口配置
"""

duankou_peizhi = duankou_peizhi.strip()
# 去除端口配置前后空格。
intface_shuju = []
# 创建端口数据列表变量，并赋值为空。
duankou_peizhi = re.split('\n', duankou_peizhi)
# 对端口配置以回车为分隔符进行分隔生成列表，配置中每行为一个列表元素。
for shuju in duankou_peizhi:
    shuju = shuju.strip()
    if not shuju.startswith('#'):
        intface_shuju.append(shuju)
# 格式化端口配置列表中元素，去除端口配置列表中每个元素的前后空格，去除以#号开关的元素，生成端口数据列表。
intface_sub = []
# 创建端口数据分片列表，并赋值为空。
yuansu_start_num = 0
# 创建分片元素开始数，并赋值为0，从第一个开始。
for yuansu_index_num in range(len(intface_shuju)):
    if intface_shuju[yuansu_index_num].startswith('interface'):
        intface_sub.append(intface_shuju[yuansu_start_num:yuansu_index_num])
        yuansu_start_num = yuansu_index_num
intface_sub.append(intface_shuju[yuansu_start_num:len(intface_shuju)])
# 以interface为标记，对端口数据列表元素时行整合。生成一个以每个子接口数据为元素的切片，并追加到intface_sub列表中。生成一个二维列表。
del intface_sub[0]
for intface_sub_shuju in intface_sub:
    print('*' * 30)
    print(intface_sub_shuju)
    print('*' * 30)
print(len(intface_sub))

