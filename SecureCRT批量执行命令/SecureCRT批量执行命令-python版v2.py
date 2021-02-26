import time
def read_file(file_path):
    with open(file_path, 'r') as file:
            data = file.read()
    return data

file_path = crt.Dialog.FileOpenDialog("请选择一个命令存放文件", "打开", "a.txt", "打开文件 (*.txt)|*.txt")

if file_path:
    list_comm = read_file(file_path).split('\n')
    crt.Screen.Synchronous = True
    for i in list_comm:
        crt.Screen.Send("\n"+i+"\n")
        while True:
            str = crt.Screen.WaitForStrings(["---- More ----","please wait..."],3)
            if str == 1:
                crt.Screen.Send(" ")
            elif str== 2:
                time.sleep(20)
            else:
                break