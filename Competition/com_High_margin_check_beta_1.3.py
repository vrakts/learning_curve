# Current Version 1.3 beta
##########################
# Reads the product codes from the competition file and compares the
# High Margin and High Stock sign existance in the CY website.
# Will only write the changes found in an xls file.
##########################
# Changelog 1.3 beta:
# - Reads from all 3 sheets at once and write only changes to three respective sheets at the end.
# - Checks if the same product code is already checked on the Singular file and skip.
# - New folder calculation function decides which folder to read from and write on
# - Attempt to trap HTTP read errors.
# Changelog Version 1.2:
# - Writes only the values that have actually changed in the xls file. If no changes are made the file will not be saved.
# Changelog Version 1.1:
# - Calculates if High Stock exists prior to High Margin
# - Writes better answers in the xls file for correct filtering
##########################
# -- To do: Retry incase of http read failure or keep the last read row and continue
#	from there in the next run, calculate average time between products.
##########################

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import urllib.request
import xlrd  # for the ability to read excel (XLS) files
import xlwt  # for the ability to write to excel (XLS) files
import ezodf  # for the ability to write to open document format (ODF) files
from datetime import date  # for the ability to get dates
import time  # for the ability to measure time
import os  # for the ability to use os functions
import os.path  # for the ability to get information on folders
import re  # for regex
import sys

##########################################
# Setting starting date and time values. #
##########################################

start_time = time.time()  # set starting time
today = date.today()  # set starting date
start_date = today.strftime("%d-%m-%Y")  # format date dd-mm-yy
print("Script started at " + start_date)
print("")

################################
# End of date and time setting #
################################

###############################
# Setting correct read paths. #
###############################

if os.path.exists(r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ') == True :  # does work folder exist?
 read_path = (r'K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ')
 print("Using " + read_path + " for reading files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder exist?
 read_path = (r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using home path 1 for reading files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder 1 exist?
 read_path = (r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using home path 2 for reading files.")
 print("")
else :
 print("No folders or files found. Where am I?")
 sys.exit()

##############################
# End of read paths setting. #
##############################

################################
# Setting correct write paths. #
################################

if os.path.exists(r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does work folder exist?
 write_path = (r"K:\SALES\ΧΡΗΣΤΕΣ\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Using " + write_path + " for writing files.")
 print("")
elif os.path.exists(r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder exist?
 write_path = (r"Z:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Home folder found but script will probably fail. Using home path 1 for writing files.")
 print("")
elif os.path.exists(r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ") == True :  # does home folder 1 exist?
 write_path = (r"W:\OneDrive\HTML Parser\PRODUCT 3 - ΓΙΩΡΓΟΣ ΒΡΑΚΑΣ")
 print("Home folder found but script will probably fail. Using home path 2 for writing files.")
 print("")
else :
 if os.path.exists(r"C:\TEMPYTH") == True :  # does temp folder exist?
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Using " + write_path + " for writing files.")
  print("")
 else :  # if not create it
  os.makedirs(r"C:\TEMPYTH")
  write_path = (r"C:\TEMPYTH")
  print("Predefined paths don't exist. Creating and using " + write_path + " for writing files.")
  print("")

###############################
# End of write paths setting. #
###############################

# Opening files
# For reading
os.chdir(read_path)
read_file = ('Ανταγωνισμός Λευκωσίας SUM.ods')  # path to ods read file
ezodf.config.set_table_expand_strategy('all')  # config ezodf to capture all content
spreadsheet = ezodf.opendoc(read_file)  # open file
ezodf.config.reset_table_expand_strategy()  # reset ezodf config
# for writing
os.chdir(write_path)
write_file = ("High_Margin_Check.xls")  # name of xls write file
alt_write_file = ("High_Margin_ALT_Check.xls")  # alternate name of xls write file
wb_write = xlwt.Workbook()  # Create a virtual workbook to keep data in
ws_write = wb_write.add_sheet("SINGULAR", cell_overwrite_ok=True)  # add 1st sheet in virtual workbook
ws_write.write(0, 0, start_date)  # write title on A1 cell
# ws_write.write(0, 1, "HMARGIN")  # write title on B1 cell

##################################
# Sheet and row/columns setting. #
##################################

# Counting rows and columns
sheets = spreadsheet.sheets
sheet1 = sheets[0]
sheet2 = sheets[1]
sheet3 = sheets[2]
rowcount1 = sheet1.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount1 = sheet1.ncols()
rowcount2 = sheet2.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount2 = sheet2.ncols()
rowcount3 = sheet3.nrows()  # for some reason the ods file reports + 3 empty rows. Add -3 at the end to remove them
colcount3 = sheet3.ncols()
ac_row1 = 1  # actual rows with data on them
ac_row2 = 1  # actual rows with data on them
ac_row3 = 1  # actual rows with data on them

# Counting rows that contain actual data (ac_row)
for i in range(1, rowcount1) :
 # print(ac_row1)
 if str(sheet1[i, 2].value) != "None" :
  ac_row1 = ac_row1 + 1
 else:
  break

for i in range(1, rowcount2) :
 # print(ac_row2)
 if str(sheet2[i, 2].value) != "None" :
  ac_row2 = ac_row2 + 1
 else:
  break

for i in range(1, rowcount3) :
 # print(ac_row3)
 if str(sheet3[i, 2].value) != "None" :
  ac_row3 = ac_row3 + 1
 else:
  break

#########################################
# End of sheet and row/columns setting. #
#########################################

ac_row1 = 10
ac_row2 = 10
ac_row3 = 10

dirty = 0  # did something change? then dirty will change to 1
e = 1  # this the write excel file position.
attempt = 0  # how many attempts to re-read the url in case of failure
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

#############################
# Parsing code starts here. #
#############################

print("")
print("Starting Singular check ...")
print("")

for i in range(1, ac_row1) :
 print("Processing singular row: " + str(i) + " / " + str(ac_row1 - 1) + ". Remaining: " + str((ac_row1 - 1) - i) + ".")
 if str(sheet1[i, 2].value.strip()) == "None" :
  break
 else :
  page_url = "http://www.eshopcy.com.cy/product?id=" + sheet1[i, 2].value.strip()
  # print(page_url)
  req = urllib.request.Request(page_url, headers = headers)
  attempt = 0
  while attempt < 3 :
   try :
    # print("On try :" + str(attempt))
    uClient = uReq(req)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    break
   except http.client.IncompleteRead :
    # print("On except :" + str(attempt))
    attempt = attempt + 1
   # else :
    # pass
  q_margin1 = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
  q_stock1 = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
  if len(q_stock1) != 0 :  # if q_stock1 not empty then stock sign exists
   print("For " + str(sheet1[i, 2].value.strip()) + " on row " + str(i+1) + " high stock exists.")
   q_text = "STOCK"
  elif len(q_margin1) == 0 :  # if q_margin1 is empty then margin sign doesn't exist and should be corrected
   print("For " + str(sheet1[i, 2].value.strip()) + " on row " + str(i+1) + " high margin doesn't exist.")
   q_text = "MARGIN"
  else :  # if both stock sign doesn't exist and high margin exist then no changes
   # print("For " + str(sheet1[i, 2].value.strip()) + " on row " + str(i+1) + " high margin exists. No changes will be made.")
   continue
  if len(q_stock1) != 0 or len(q_margin1) == 0 :
   ws_write.write(e, 0, sheet1[i, 2].value.strip())
   ws_write.write(e, 1, q_text)
   # ws_write.write(0, 1, str(sheet1[i, 2].value.strip()))
   e = e + 1
   dirty = 1
  ws_write.write(0, 1, str(sheet1[i, 2].value.strip()))
  # print("Processing Singular row: " + str(i) + "/" + str(ac_row1) + ". Remaining: " + str(ac_row1 - i))

ws_write = wb_write.add_sheet("ELECTROLINE", cell_overwrite_ok=True)
ws_write.write(0, 0, start_date)  # write date on A1 cell
check_status = 0
e = 1

print("")
print("Starting Electroline check ...")
print("")

for i in range(1, ac_row2) :
 print("Processing Electroline row: " + str(i) + " / " + str(ac_row2 - 1) + ". Remaining: " + str((ac_row2 - 1) - i) + ".")
 if str(sheet2[i, 2].value.strip()) == "None" :
  break
 else :
  for check in range (1, ac_row1) :
   if sheet2[i, 2].value.strip() != sheet1[check, 2].value.strip() :
    check_status = 0  # not found
    # print(check_status)
   else :
    check_status = 1  # found
    # print(check_status)
  if check_status == 0 :
   page_url = "http://www.eshopcy.com.cy/product?id=" + sheet2[i, 2].value.strip()
   # print(page_url)
   req = urllib.request.Request(page_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     uClient = uReq(req)
     page_soup = soup(uClient.read(), "html.parser")
     uClient.close()
     break
    except http.client.IncompleteRead :
     # print("On except :" + str(attempt))
     attempt = attempt + 1
    # else :
     # pass
   q_margin2 = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
   q_stock2 = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
   if len(q_stock2) != 0 :  # if q_stock2 not empty then stock sign exists
    print("For " + str(sheet2[i, 2].value.strip()) + " on row " + str(i+1) + " high stock exists.")
    q_text = "STOCK"
   elif len(q_margin2) == 0 :  # if q_margin1 is empty then margin sign doesn't exist and should be corrected
    print("For " + str(sheet2[i, 2].value.strip()) + " on row " + str(i+1) + " margin doesn't exist.")
    q_text = "MARGIN"
   else: 
    # print("For " + str(sheet2[i, 2].value.strip()) + " on row " + str(i+1) + " high margin exists. No changes will be made.")
    continue
   # print("Processing Electroline row: " + str(i) + "/" + str(ac_row2) + ". Remaining: " + str(ac_row2 - i))
  if len(q_stock2) != 0 or len(q_margin2) == 0 :
   ws_write.write(e, 0, sheet2[i, 2].value.strip())
   ws_write.write(e, 1, q_text)
   # ws_write.write(0, 1, str(sheet2[i, 2].value.strip()))
   e = e + 1
   dirty = 1
  else :
   pass
  ws_write.write(0, 1, str(sheet2[i, 2].value.strip()))

ws_write = wb_write.add_sheet("CUSTOMPC", cell_overwrite_ok=True)
ws_write.write(0, 0, start_date)  # write date on A1 cell
check_status = 0
e = 1

print("")
print("Starting CustomPC check ...")
print("")

for i in range(1, ac_row3) :
 print("Processing CustomPC row: " + str(i) + " / " + str(ac_row3 - 1) + ". Remaining: " + str((ac_row3 - 1) - i) + ".")
 if str(sheet3[i, 2].value.strip()) == "None" :
  break
 else :
  for check in range (1, ac_row1) :
   # print("Looping: " + str(check) + " and " + str(i))
   if sheet3[i, 2].value.strip() != sheet1[check, 2].value.strip() :
    check_status = 0  # not found
    # print(check_status)
   else :
    check_status = 1  # found
    # print(check_status)
  if check_status == 0 :
   page_url = "http://www.eshopcy.com.cy/product?id=" + sheet3[i, 2].value.strip()
   req = urllib.request.Request(page_url, headers = headers)
   attempt = 0
   while attempt < 3 :
    try :
     # print("On try :" + str(attempt))
     uClient = uReq(req)
     page_soup = soup(uClient.read(), "html.parser")
     uClient.close()
     break
    except http.client.IncompleteRead :
     # print("On except :" + str(attempt))
     attempt = attempt + 1
    # else :
     # pass
   q_margin3 = page_soup.findAll("font", {"style" : "color:#ff9933;font-weight:bold;font-size:9px;font-family:arial black;"})
   q_stock3 = page_soup.findAll("font", {"style" : "color:#ff0000;font-weight:bold;font-size:9px;font-family:arial black;"})
   if len(q_stock3) != 0 :  # if q_stock3 not empty then stock sign exists
    print("For " + str(sheet3[i, 2].value.strip()) + " on row " + str(i+1) + " high stock exists.")
    q_text = "STOCK"
   elif len(q_margin3) == 0 :  # if q_margin3 is empty then margin sign doesn't exist and should be corrected
    print("For " + str(sheet3[i, 2].value.strip()) + " on row " + str(i+1) + " margin doesn't exist.")
    q_text = "MARGIN"
   else: 
    # print("For " + str(sheet3[i, 2].value.strip()) + " on row " + str(i+1) + " high margin exists. No changes will be made.")
    continue
   # print("Processing CustomPC row: " + str(i) + "/" + str(ac_row3) + ". Remaining: " + str(ac_row3 - i))
  if len(q_stock3) != 0 or len(q_margin3) == 0 :
   ws_write.write(e, 0, sheet3[i, 2].value.strip())
   ws_write.write(e, 1, q_text)
   # ws_write.write(0, 1, str(sheet3[i, 2].value.strip()))
   e = e + 1
   dirty = 1
  else :
   pass
  ws_write.write(0, 1, str(sheet3[i, 2].value.strip()))

########################
# End of parsing code. #
########################

# try to write to the 1st file. If it fails try the 2nd
try :
 wb_write.save(write_file)
except :
 wb_write.save(alt_write_file)

if dirty == 0 :
 print("Results are not dirty. No changes made.")
 pass
else :
 print("Results are dirty. Writing changes to file.")
 try :
  wb_write.save(write_file)
 except :
  wb_write.save(alt_write_file)
  
#############################
# Calculating elapsed time. #
#############################

elapsed_time = time.time() - start_time
minutes = elapsed_time / 60  # σωστό, μας δίνει τα λεπτά και δεκαδικό για τα δεύτερα.
mins, delim, seconds = str(minutes).partition(".")  # σωστό, χωρίζει το χρόνο σε λεπτά, άχρηστα τα "." και δεύτερα
seconds = round(elapsed_time, 0) - int(mins) * 60  # σωστό, αφαιρούμε όλο τον χρόνο - τα λεπτά σε δεύτερα^
seconds, delim, mseconds = str(seconds).partition(".")  # σωστό, χωρίζει τα δεύτερα σε λεπτά, άχρηστα τα "." και msec
formatted_time = (str(mins) + " minutes and " + str(seconds) + " seconds (" + str(round(elapsed_time, 2)) + " seconds).")
print("Script executed in: " + formatted_time)

################
# End of flie. #
################

