import ctypes
import sys
import os
from calendar import monthrange
from datetime import date
from datetime import datetime

def get_deets() :
 operations = []
 i = 0
 answer = ""
 # while answer != "_____" or answer != "www.e-shop.gr" or answer != "end" :
 while answer.find("_____") < 0 or answer.find("www.e-shop.gr") < 0 or answer.find("end") < 0 :
  answer = input("Paste values: ")
  answer = answer.replace('•', '').strip()
  while answer.find('  ') >= 0 :
   answer = remove_spaces(answer)
  # print(answerend)
  
  if answer == '' :
   continue
  else :
   operations.append(answer)
 
 for t in operations :
  # if t == "" :
   # print("empty")
  # else :
   # pass
  print(">"+ t + "<")
 
 file = open("operations.txt", "a")
 for l in operations :
  file.write(l + "\n")
 
 file.close()
 
 return(operations)

def set_date() :
 global today, cur_day, cur_month, cur_year, custom_date, current_time, num_days
 today = date.today()
 cur_day = date.today().day
 cur_month = date.today().month
 cur_year = today.strftime("%y")
 custom_date = str(cur_day) + "/" + str(cur_month) + "/" + str(cur_year)
 custom_date = today.strftime("%d/%m/%Y")
 now = datetime.now()
 current_time = now.strftime("%H:%M")
 num_days = monthrange(int(cur_year), int(cur_month))[1]

def remove_spaces(txt) :
 txt = txt.replace('  ', ' ')
 return(txt)

try :
 set_date()
 print(today)
 date_exists = False
 dates = []
 strip_lines = []
 write_path = r"Z:\OneDrive\eShop Stuff\PRODUCT\Product"
 print("")

 os.chdir(write_path)
 if os.path.exists(os.getcwd() + "\\operations.txt") == True :
  file = open("operations.txt", "r")
  Lines = file.readlines()
  file.close()
  for line in Lines :
   while line.find('  ') >= 0 :
    line = remove_spaces(line)
   strip_lines.append(line.strip())
  
  for line in strip_lines :
   if line.find('/') >= 0 :
    temp_date = line[line.rfind(',') + 1:].strip()
    dates.append(temp_date.strip())
   else :
    pass
 else :
  pass
 
 if len(dates) > 0 :
  for d in dates :
   print(d)
   if custom_date <= d :
    date_exists = True
   else :
    date_exists = False
  # print(date_exists)
 else :
  date_exists = False
 
 date_exists
 
 if date_exists == False :
  print("Operations text file has older or no dates and needs to be updated. Please paste all lines from the e-mail until signature's address to continue.")
  print("")
  operations = get_deets()

 for i in range(0, len(strip_lines)) :
  line = strip_lines[i]
  temp_date = line[line.rfind(',') + 1:].strip()
  if temp_date == custom_date :
   print('---> ' + line.strip() + ' <---')
   for j in range(i, len(strip_lines)) :
    next_line = strip_lines[j + 1].strip()
    if next_line.find(':') >= 0 and next_line.find('-') >= 0 :
     min_time = next_line[next_line.find(',') + 1:next_line.find('-')].strip()
     max_time = next_line[next_line.rfind('-') + 1:].strip()
     if min_time <= current_time and max_time >= current_time :
      print(next_line)
      ctypes.windll.user32.MessageBoxW(0, next_line, "next_line", 0)
      break
    else :
     continue

 # for i in range(0, len(strip_lines)) :
  # line = strip_lines[i]
  # temp_date = line[line.rfind(',') + 1:].strip()
  # if temp_date == custom_date :
   # print('---> ' + line.strip() + ' <---')
   # for j in range(i, len(strip_lines)) :
    # next_line = strip_lines[j + 1].strip()
    # if next_line.find('/') >= 0 or next_line.find('_____') >= 0 :
     # break
    # else :
     # print(next_line)

except Exception as exc :
 print("Exception: " + str(exc) + ".")
 print("Probably write path or file not found.")
 sys.exit(1)

