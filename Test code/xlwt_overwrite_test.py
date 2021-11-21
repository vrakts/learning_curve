# - Functions tried:
# - Open the write file with append ability
#	to do that create a copy of it --- done
#	store the last i number so it can be retrieved later --- done
#	save every 10 rows read. probably needs to start the process ->
#	-> of reading and writing on each divisible i --- done
#	if the stored i is smaller than the last ac_row ->
#	-> continue from there --- done
#	now need to find a way to determine if the file exists ->
#	-> to open it up or create a new one. Try and except? --- done

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from urllib.request import quote
import urllib.request
from xlutils.copy import copy
from xlrd import open_workbook
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to write to open document format (ODF) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
 write_path = (r"C:\TEMPYTH")
 print("Predefined paths don't exist. Using " + write_path + " for writing files.")
 print("")
else :  # if not create it
 os.makedirs(r"C:\TEMPYTH")
 write_path = (r"C:\TEMPYTH")
 print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")
 print("")

# Opening files
# ods read file
os.chdir(r"Z:\OneDrive\HTML Parser\ΑΝΤΑΓΩΝΙΣΜΟΣ\Ανταγωνισμός Λευκωσίας")
read_file = ('SINGULAR - ΓΙΩΡΓΟΣ.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config


# Counting rows and columns
sheets = spreadsheet.sheets
sheet = sheets[0]
rowcount = sheet.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount = sheet.ncols()
ac_row = 1
# Counting rows that contain actual data (ac_row)
for i in range(1, rowcount):
 if str(sheet[i, 0].value) != "None" :
  ac_row = ac_row + 1
 else:
  break

# reading xls file
os.chdir(write_path)
write_file = ("test_save_file.xls")  # name of xls write file
alt_write_file = ("test_save_file_alt.xls")  # alternate name of xls write file
try: 
 print("Trying to open file: " + write_file + "...")
 wb_read = open_workbook(write_file, formatting_info=True)
 ws_read = wb_read.sheet_by_index(0)
 # ws_read_rows = ws_read.nrows
 # for writing
 wb_write = copy(wb_read) 
 ws_write = wb_write.get_sheet(0)
 print("... success. Using last known row.")
 if ws_read.cell_value(0, 2) == "" :
  last_read = 1
 else :
  last_read = int(ws_read.cell_value(0, 2))
 file_is_there = 1
except :
 print("File: " + write_file + " not found. Creating one now.")
 wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
 ws_write = wb_write.add_sheet(start_date, cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
 # ws_write.write(0, 2, 1)  # write title on B1 cell
 last_read = 1
 file_is_there = 0

ws_write.write(0, 0, "Number")  # write title on A1 cell
ws_write.write(0, 1, "Is Divisible")  # write title on B1 cell

if last_read < ac_row and last_read > 0 :
 start_from = last_read
else :
 start_from = 1

print("Starting from row: " + str(start_from))

for i in range (start_from, ac_row):
 print("i = " + str(i))
 ws_write.write(0, 2, i)  # write the current row on C1
 ws_write.write(0, 3, str(sheet[i, 0].value).strip())  # write the PER value on D1
 ws_write.write(i, 0, str(sheet[i, 0].value).strip())  # write the PER value on the first cell of current row. Only for test purposes.
 if (i % 10) == 0 :
  print(str(i) + " is divisible by 10.")
  print("")
  ws_write.write(i, 1, "yes")
  wb_write.save(write_file)
  wb_read = open_workbook(write_file, formatting_info=True)
  wb_write = copy(wb_read) 
  ws_write = wb_write.get_sheet(0)
 else :
  print(str(i) + " is NOT divisible by 10.")
  print("")
  ws_write.write(i, 1, "no")
 time.sleep(0.5)

wb_write.save(write_file)
if file_is_there == 1 :
 print("Updated file: " + write_file)
else :
 print("Saved file: " + write_file)

