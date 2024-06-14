import subprocess

# 在新的命令提示符窗口中启动另一个Python脚本执行训练，并将信息显示在窗口中
subprocess.Popen(["start", "cmd", "/k", "python", "train.py"], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
