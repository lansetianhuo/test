import time


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


file_path = crt.Dialog.FileOpenDialog(
    "请选择一个命令存放文件", "打开", "a.txt", "打开文件 (*.txt)|*.txt")
rowIndex = crt.Screen.CurrentRow
colIndex = crt.Screen.CurrentColumn - 1
prompt = crt.Screen.Get(rowIndex, 0, rowIndex, colIndex)
prompt = prompt.strip()
dev_name_flag = crt.Dialog.MessageBox(
    "请确认设备名是否为：" + str(prompt), "设备名确认", 64 | 4)
if file_path and prompt:
    if dev_name_flag != 7:
        list_comm = read_file(file_path).split('\n')
        crt.Screen.Synchronous = True
        crt.Screen.IgnoreEscape = True
        flag = "true"
        for i in list_comm:
            crt.Screen.Send(i + '\n')
            while True:
                str = crt.Screen.WaitForStrings(
                    [prompt, "---- More ----", "--More--", "please wait..."], 20)
                if str == 1:
                    break
                elif str == 2 or str == 3:
                    crt.Screen.Send(" ")
                elif str == 4:
                    time.sleep(20)
                else:
                    crt.Dialog.MessageBox("提示符内容错误", "错误信息", 16 | 0)
                    flag = "false"
                    break
            if flag == "false":
                break
