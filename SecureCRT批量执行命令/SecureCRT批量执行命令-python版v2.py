import time


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


file_path = crt.Dialog.FileOpenDialog(
    "请选择一个命令存放文件", "打开", "a.txt", "打开文件 (*.txt)|*.txt")
dev_name = str(crt.Dialog.Prompt("请输入设备提示名", "设备提示名", ""))
dev_name_flag = crt.Dialog.MessageBox("请确认设备名是否为：" + dev_name, "设备名确认", 64 | 4)
if file_path and dev_name:
    if dev_name_flag != 7:
        list_comm = read_file(file_path).split('\n')
        crt.Screen.Synchronous = True
        crt.Screen.IgnoreEscape = True
        flag = "true"
        for i in list_comm:
            crt.Screen.Send(i + '\n')
            while True:
                str = crt.Screen.WaitForStrings(
                    ["---- More ----", "please wait...", dev_name], 20)
                if str == 1:
                    crt.Screen.Send(" ")
                elif str == 2:
                    time.sleep(20)
                elif str == 3:
                    break
                else:
                    crt.Dialog.MessageBox("设备提示名错误", "错误信息", 16 | 0)
                    flag = "false"
                    break
            if flag == "false":
                break
