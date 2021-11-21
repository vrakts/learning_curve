def ti_paizei() :
 version = "Version 1.1 stable"
 # Ελέγχει το stock αρχείο αν υπάρχει ο κωδικός που κάνει copy ο χρήστης
 ### Changelog 1.1
 # Ελέγχει μόνο στο 1ο φύλο (stock) και αναφέρει σε ποιά θέση βρίσκεται το προϊόν.
 # Αν δεν βρεί τον φάκελο προσπαθεί να τον ενώσει επιτόπου.
 ###
 # στο Advanced -> --hiddenimport προσθέτεις το "pywin32"
 ###
 ###
 # Use this to disconnect K: drive
 # subprocess.call(r'net use K: /del', shell=True)
 # Use this to reconnect K: drive
 # subprocess.call(r'net use K: \\shared-nic\NetHDD', shell=True)
 ###
 print(version)

from bs4 import BeautifulSoup as soup  # HTML data structure
import ezodf
import os
import sys
import clipboard
import win32ui
import win32con
import subprocess

try:
 found = 0
 s_text = clipboard.paste().strip()
 
 if s_text == "" :
  print("Δεν έχω σπίτι ούτε πατρίδα.")
  win32ui.MessageBox("Δεν έχεις αντιγράψει τον κωδικό.", "Δεν έχω σπίτι ούτε πατρίδα", win32con.MB_OK)
  sys.exit(0)
 
 read_path1 = (r"K:\Sales\Stock")
 read_path2 = (r"Z:\Users\Vrakts\Desktop")
 retry = 1
 attempt = 0 
 path_flag = True

 while path_flag == True :
  try :
   if os.path.exists(read_path1) == True :
    os.chdir(read_path1)
    path_flag = False
   else :
    os.chdir(read_path2)
    path_flag = False
  except Exception as exc :
   if attempt == retry :
    win32ui.MessageBox("Exception: " + str(exc), "Ξεσκιούζ μι...", win32con.MB_OK)
    sys.exit(str(exc))
   elif str(exc).find("[WinError 3] The system cannot find the path specified") >= 0 :
    print("Αφαιρώ κοινόχρηστα...")
    subprocess.call(r'net use K: /del', shell = True)
    print("Προσθέτω κοινόχρηστα...")
    subprocess.call(r'net use K: \\shared-nic\NetHDD', shell = True)
    attempt += 1
 
 read_file = ('Stock.ods')
 ezodf.config.set_table_expand_strategy('all')
 spreadsheet = ezodf.opendoc(read_file)
 ezodf.config.reset_table_expand_strategy()
 sheets = spreadsheet.sheets
 
 sheet1 = sheets[0]
 rowcount1 = sheet1.nrows()
 colcount1 = sheet1.ncols()
 ac_row1 = 1
 
 for i in range(1, rowcount1) :
  if str(sheet1[i, 0].value) != "None" :
   ac_row1 += 1
  else:
   break
 
 for i in range(0, ac_row1) :
  if str(sheet1[i, 0].value.strip()) == "None" :
   break
  elif str(sheet1[i, 0].value.strip()) == s_text :
   for v in range(i, ac_row1) :
    if str(sheet1[v, 0].value.strip()) == str(sheet1[i, 0].value.strip()) :
     found += 1
    else :
     break
   break 
 if found == 1 :
  print_text = "Υπάρχει " + str(found) + " τεμάχιο " + s_text + " στην περιοχή " + sheet1[i, 10].value
  win32ui.MessageBox(print_text, "Το βρήκα", win32con.MB_OK)
 elif found > 1 :
  print_text = "Υπάρχουν " + str(found) + " τεμάχια " + s_text + " στην περιοχή " + sheet1[i, 10].value
  win32ui.MessageBox(print_text, "Το βρήκα", win32con.MB_OK)
 else :
  print_text = "Το " + s_text + " δεν υπάρχει στο αρχείο."
  win32ui.MessageBox("Το " + s_text + " δεν υπάρχει στο αρχείο.", "Τι να κάνεις; Να μαλώεις;", win32con.MB_OK)
except Exception as exc :
 print("Exception: " + str(exc))
 win32ui.MessageBox("Exception: " + str(exc), "Ξεσκιούζ μι...", win32con.MB_OK)
