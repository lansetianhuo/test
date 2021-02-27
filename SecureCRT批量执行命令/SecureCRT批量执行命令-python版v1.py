def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


file_path = crt.Dialog.FileOpenDialog(
    "请选择一个命令存放文件", "打开", "a.txt", "打开文件 (*.txt)|*.txt")


if file_path:
    list_comm = read_file(file_path).split('\n')

    crt.Screen.Synchronous = True
    rowIndex = crt.Screen.CurrentRow
    colIndex = crt.Screen.CurrentColumn - 1
    prompt = crt.Screen.Get(rowIndex, 0, rowIndex, colIndex)
    prompt = prompt.strip()
    flag = "true"
    for i in list_comm:
        crt.Screen.Send(i + "\n")
        while True:
            str = crt.Screen.WaitForStrings(
                [prompt, "---- More ----", "--More--"], 25)
            if str == 1:
                break
            elif str == 2 or str == 3:
                crt.Screen.Send(" ")
            else:
                crt.Dialog.MessageBox("设备提示名错误", "错误信息", 16 | 0)
                flag = "false"
                break
        if flag == "false":
            break
