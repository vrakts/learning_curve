try :
 import sys
 import os
 import pyautogui
 import clipboard
 from random import randint
 from time import sleep as nani
except KeyboardInterrupt :
 import sys
 sys.exit(0)
except Exception as exc :
 import sys
 print("Κάτι πάθαμε κατά το import.")
 print(str(exc))
 sys.exit(0)

def refresh() :
 pyautogui.moveTo(20, 20, duration = move_duration)
 pyautogui.click()
 pyautogui.press('F6')
 nani(move_duration)
 pyautogui.typewrite('https://www.banggood.com/Casual-Game-Money-Box.html', interval = type_interval)
 nani(move_duration)
 pyautogui.press('F6')
 nani(move_duration)
 pyautogui.press('F6')
 nani(move_duration)
 # pyautogui.keyDown('ctrlleft')
 # nani(move_duration)
 # pyautogui.press('c')
 # nani(move_duration)
 # pyautogui.keyUp('ctrlleft')
 # nani(move_duration)
 pyautogui.hotkey('ctrl', 'c')
 copy_text = clipboard.paste().strip()
 print(copy_text)
 input()
 if copy_text.find('ηττπσ') >= 0 or copy_text.find('//../') >= 0 :
  pyautogui.keyDown('altleft')
  nani(move_duration)
  pyautogui.press('shiftleft')
  nani(move_duration)
  pyautogui.keyUp('altleft')
  nani(move_duration)
  pyautogui.press('F6')
  nani(move_duration)
  pyautogui.typewrite('https://www.banggood.com/Casual-Game-Money-Box.html', interval = type_interval)
 else :
  pass
 pyautogui.press('enter')

def click_it() :
 pyautogui.moveTo(randint(20,100), randint(20,100), duration = move_duration)
 nani(0.5)
 pyautogui.moveTo(randint(580,760), randint(680,700), duration = move_duration)
 nani(1)
 pyautogui.click()
 # return(0)

try:
 run = 0
 move_duration = 0.2
 type_interval = 0.1
 # refresh_random = 0
 print('Press Ctrl-C to quit.')

 refresh()
 nani(6)
 
 while True:
  refresh_random = 0
  run += 1
  if run == 1 :
   wait = 1
  else :
   wait = randint(101,10000)
  
  for i in range (1, wait) :
   os.system('cls')
   print("Γύρος: " + str(run))
   print("Περιμένω για " + str(i) + "/" + str(wait) + " δεύτερα.")

   diff = wait - i
   if refresh_random == 0 :
    refresh_random = int(wait / 3)
   elif diff > 50 and diff % refresh_random == 0:   # possibly needs OR?
    refresh()
   else :
    pass

   print('Press Ctrl-C to quit.')
   print("")
   print("Απομένουν:     " + str(diff) + " δεύτερα")
   print("Ανανέωση κάθε: " + str(refresh_random) + " δεύτερα")
   print("Ανανεώνω σε:   " + str(diff % refresh_random))
   
   # if diff > 100 or refresh_random != 0 :
    # if diff % randint(100, diff) == 0 :
     # refresh()
    # else :
     # pass
   # else :
    # refresh_random = randint(100, diff)

   if diff == 10 :
    refresh()
    refresh_random = 0
   else :
    pass

   nani(1)
  click_it()

except KeyboardInterrupt:
 print('\nΤέλος.')
