from bs4 import BeautifulSoup as soup  # HTML data structure
# from pynput import keyboard
import ezodf, time, os, re, sys, clipboard, ctypes

# pyautogui.hotkey("ctrlleft", "a")

found = 0

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

# Sheet 1 specs
sheet1 = sheets[0]
rowcount1 = sheet1.nrows()
colcount1 = sheet1.ncols()
ac_row1 = 1

# Sheet 2 specs
sheet2 = sheets[1]
rowcount2 = sheet2.nrows()
colcount2 = sheet2.ncols()
ac_row2 = 1

# Sheet 3 specs - don't use
# sheet3 = sheets[2]
# rowcount3 = sheet3.nrows()
# colcount3 = sheet3.ncols()
# ac_row3 = 1

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

# for i in range(1, rowcount3) :
 # # print(ac_row3)
 # if str(sheet3[i, 0].value) != "None" :
  # ac_row3 += 1
 # else:
  # break

for i in range(0, ac_row1) :
 # print(str(sheet1[i, 0].value.strip()))
 # print(s_text)
 if str(sheet1[i, 0].value.strip()) == "None" :
  break
 elif str(sheet1[i, 0].value.strip()) == s_text :
  # print(str(sheet1[i, 0].value.strip()))
  # print("Υπάρχει στο στοκ.")
  for v in range(i, ac_row1) :
   if str(sheet1[v, 0].value.strip()) == str(sheet1[i, 0].value.strip()) :
    found += 1
   else :
    break
  if found == 1 :
   print_text = "Υπάρχει " + str(found) + " τεμάχιο " + s_text + " στο " + sheet1.name
  else :
   print_text = "Υπάρχουν " + str(found) + " τεμάχια " + s_text + " στο " + sheet1.name
  ctypes.windll.user32.MessageBoxW(0, print_text, "Το βρήκα", 0)
  sys.exit(0)

for i in range(0, ac_row2) :
 # print(str(sheet2[i, 0].value.strip()))
 # print(s_text)
 if str(sheet2[i, 0].value.strip()) == "None" :
  break
 elif str(sheet2[i, 0].value.strip()) == s_text :
  # print("Υπάρχει στο crazy.")
  for v in range(i, ac_row2) :
   if str(sheet2[v, 0].value.strip()) == str(sheet2[i, 0].value.strip()) :
    found += 1
   else :
    break
  if found == 1 :
   print_text = "Υπάρχει " + str(found) + " τεμάχιο " + s_text + " στο " + sheet2.name + " (τρέχων)."
  else :
   print_text = "Υπάρχουν " + str(found) + " τεμάχια " + s_text + " στο " + sheet2.name + " (τρέχων)."
  ctypes.windll.user32.MessageBoxW(0, print_text, "Το βρήκα", 0)
  sys.exit(0)
 
# for i in range(0, ac_row3) :
 # # print(str(sheet3[i, 0].value.strip()))
 # # print(s_text)
 # if str(sheet3[i, 0].value.strip()) == "None" :
  # break
 # elif str(sheet3[i, 0].value.strip()) == s_text :
  # # print("Υπάρχει στο crazy.")
  # for v in range(i, ac_row3) :
   # if str(sheet3[v, 0].value.strip()) == str(sheet3[i, 0].value.strip()) :
    # found += 1
   # else :
    # break
  # if found == 1 :
   # print_text = "Υπάρχει " + str(found) + " τεμάχιο " + s_text + " στο " + sheet3.name + " (επόμενο)."
  # else :
   # print_text = "Υπάρχουν " + str(found) + " τεμάχια " + s_text + " στο " + sheet3.name + " (επόμενο)."
  # ctypes.windll.user32.MessageBoxW(0, print_text, "Το βρήκα", 0)
  # sys.exit(0)

# print("Δεν υπάρχει στο αρχείο.")
ctypes.windll.user32.MessageBoxW(0, "Το " + s_text + " δεν υπάρχει στο αρχείο.", "Τι να κάνεις; Να μαλώεις;", 0)
# input()