import shelve


def read_data(data_file, data_name):
    data = shelve.open(data_file)
    original_data = data[data_name]
    data.close()
    return original_data


def write_data(file_name, data_name, data):
    stud_db = shelve.open(file_name)
    stud_db[data_name] = data
    stud_db.close()


def intf_list_collect(dev_data_list):
    intf_data_list = []
    for dev_data_row in dev_data_list:
        if len(dev_data_row) > 0:
            if dev_data_row[0].startswith('interface'):
                intf_data_list.append(dev_data_row)
    return intf_data_list


def main():
    data_file = r'D:\xuexi\db\dev_data_db'
    read_data_name = 'dev_data_list'
    write_data_name = 'intface_data_list'
    dev_data_list = read_data(data_file, read_data_name)
    intf_data_list = intf_list_collect(dev_data_list)

    write_data(data_file, write_data_name, intf_data_list)


if __name__ == '__main__':
    main()
