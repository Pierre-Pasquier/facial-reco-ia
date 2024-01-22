from time import sleep
import os

print("signal handler ON")

try:
    while 1 : sleep(10) 
except KeyboardInterrupt:
    pass
finally:
    print("KeyboardInterrupt")
    print("signal handler OFF")
    os.system("pkill -9 python3")
