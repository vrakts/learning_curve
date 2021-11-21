from bs4 import BeautifulSoup as soup  # HTML data structure
from pynput import keyboard
import ezodf, time, os, re, sys, clipboard, ctypes

# pyautogui.hotkey("ctrlleft", "a")

s_text = clipboard.paste().strip()
# s_text = "PER.111111"
# print(s_text)

if s_text == "" :
 print("Δεν έχω σπίτι ούτε πατρίδα.")
 ctypes.windll.user32.MessageBoxW(0, "Δεν έχεις αντιγράψει τον κωδικό.", "Δεν έχω σπίτι ούτε πατρίδα", 0)
 sys.exit(0)

read_path1 = (r"K:\Sales\Stock")
read_path2 = (r"Z:\Users\Vrakts\Desktop")
try :
 os.chdir(read_path1)
except Exception:
 os.chdir(read_path2)
read_file = ('Stock.ods')
ezodf.config.set_table_expand_strategy('all')
spreadsheet = ezodf.opendoc(read_file)
ezodf.config.reset_table_expand_strategy()
sheets = spreadsheet.sheets
sheet1 = sheets[0]
sheet2 = sheets[1]
rowcount1 = sheet1.nrows()
colcount1 = sheet1.ncols()
rowcount2 = sheet2.nrows()
colcount2 = sheet2.ncols()
ac_row1 = 1
ac_row2 = 1

for i in range(1, rowcount1) :
 # print(ac_row1)
 if str(sheet1[i, 0].value) != "None" :
  ac_row1 += 1
 else:
  break

for i in range(1, rowcount2) :
 # print(ac_row2)
 if str(sheet2[i, 0].value) != "None" :
  ac_row2 += 1
 else:
  break

for i in range(0, ac_row1) :
 # print(str(sheet1[i, 0].value.strip()))
 # print(s_text)
 if str(sheet1[i, 0].value.strip()) == "None" :
  break
 elif str(sheet1[i, 0].value.strip()) == s_text :
  # print(str(sheet1[i, 0].value.strip()))
  print("Υπάρχει στο στοκ.")
  ctypes.windll.user32.MessageBoxW(0, "Το " + s_text + " υπάρχει στο στοκ.", "Το βρήκα", 0)
  sys.exit(0)

for i in range(0, ac_row2) :
 # print(str(sheet1[i, 0].value.strip()))
 # print(s_text)
 if str(sheet2[i, 0].value.strip()) == "None" :
  break
 elif str(sheet2[i, 0].value.strip()) == s_text :
  print("Υπάρχει στο crazy.")
  ctypes.windll.user32.MessageBoxW(0, "Το " + s_text + " υπάρχει στο crazy.", "Το βρήκα", 0)
  sys.exit(0)

print("Δεν υπάρχει στο αρχείο.")
ctypes.windll.user32.MessageBoxW(0, "Το " + s_text + " δεν υπάρχει στο αρχείο.", "Τί να κάνεις; Να τσακωθείς;", 0)
