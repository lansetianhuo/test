def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


file_path = crt.Dialog.FileOpenDialog(
    "请选择一个命令存放文件", "打开", "a.txt", "打开文件 (*.txt)|*.txt")
list_comm_exc = ['display elabel', 'display patch-information']
if file_path:
    list_comm = read_file(file_path).split('\n')
    crt.Screen.Synchronous = True
    for i in list_comm:
        if i in list_comm_exc:
            crt.Screen.Send("\n" + i + "\n")
            while (crt.Screen.WaitForStrings(["---- More ----"], 20)):
                crt.Screen.Send(" ")
        else:
            crt.Screen.Send("\n" + i + "\n")

            while (crt.Screen.WaitForStrings(["---- More ----"], 2)):
                crt.Screen.Send(" ")