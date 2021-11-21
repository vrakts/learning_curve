# mouseNow.py - Displays the mouse cursor's current position.
import pyautogui
print('Press Ctrl-C to quit.')
try:
 while True:
  # TODO: Get and print the mouse coordinates.
  # Get and print the mouse coordinates + RGB color.
  # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
  # print(positionStr, end='')
  # print('\b' * len(positionStr), end='', flush=True)
  x, y = pyautogui.position()
  positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
  pixelColor = pyautogui.screenshot().getpixel((x, y))
  positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
  positionStr += ', ' + str(pixelColor[1]).rjust(3)
  positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
  # print(positionStr, end=' ' )
  print(positionStr)
except KeyboardInterrupt:
 print('\nDone.')

# print(positionStr, end='')
# print('\b' * len(positionStr), end='', flush=True)




"""
580 680
760 700
"""