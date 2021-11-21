import pyautogui
import sys

try:
    while True:
        x,y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='\r')
except KeyboardInterrupt:
    print("")
except Exception as exc:
    print("Exception:", exc)
    sys.exit(1)