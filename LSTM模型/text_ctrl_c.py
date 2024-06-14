# 测试ctrl+c中断是否可以
import time

try:
    while True:
        print("Hello")
        time.sleep(1)

except KeyboardInterrupt:
    print("中断")